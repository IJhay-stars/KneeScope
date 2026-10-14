"""Validate and render the KneeScope backlog.

Source: docs/issues/src/*.toml (hand-edited). Outputs (generated, do not edit):
  docs/issues/<ID>.md        one issue body per actionable issue and epic
  docs/issues/manifest.json  machine-readable manifest (used by publish_issues.py)
  docs/issues/manifest.md    human-readable table with dependencies and status

Usage:
  python scripts/backlog.py check    # validate fields, references and the dependency DAG
  python scripts/backlog.py render   # check, then write the generated files
  python scripts/backlog.py ready    # list issues whose prerequisites are all closed
"""

from __future__ import annotations

import json
import sys
import tomllib
from graphlib import CycleError, TopologicalSorter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "issues" / "src"
OUT = ROOT / "docs" / "issues"
STATE = OUT / "state.json"  # {"closed": [...], "triggered": {...}} maintained by humans/agents

REQUIRED = [
    "id",
    "title",
    "epic",
    "type",
    "priority",
    "workstream",
    "owner_role",
    "depends_on",
    "problem",
    "outcome",
    "scope",
    "guidance",
    "files",
    "contract_impact",
    "acceptance",
    "verification",
    "docs",
    "dod",
]
TYPES = {"task", "decision", "conditional", "optional"}
PRIORITIES = {"P0", "P1", "P2"}
SCIENCE_KEYS = ["dataset", "partition", "metrics", "cannot_claim", "artifacts"]
SCIENCE_WORKSTREAMS = {"modelling", "evaluation", "labels"}
UI_WORKSTREAMS = {"frontend"}
VAGUE = ["looks good", "works correctly", "production ready", "works as expected", "is fast"]

COMMON_DOD = [
    "Every acceptance criterion is met and the evidence (test names, command output, screenshots, links) is posted in the issue or PR.",
    "Verification commands pass locally and in CI where CI covers them.",
    "Listed documentation is updated in the same PR; DESIGN.md/contracts changes follow AGENTS.md procedures.",
    "PR reviewed by someone from a different workstream; no restricted data, credentials or large binaries committed.",
    "docs/issues/state.json and docs/issue-index.md updated (status, links).",
]


def load() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    epics: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    for path in sorted(SRC.glob("*.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        epics += data.get("epic", [])
        for issue in data.get("issue", []):
            issue["_source"] = path.name
            issues.append(issue)
    return epics, issues


def state() -> dict[str, Any]:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))  # type: ignore[no-any-return]
    return {"closed": [], "triggered": {}}


def validate(epics: list[dict[str, Any]], issues: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    epic_ids = {e["id"] for e in epics}
    ids = [i.get("id") for i in issues]
    for dup in {x for x in ids if ids.count(x) > 1}:
        errors.append(f"duplicate id {dup}")
    known = set(ids)
    for i in issues:
        iid = i.get("id", "?")
        for key in REQUIRED:
            if key not in i or i[key] in ("", None):
                errors.append(f"{iid}: missing field {key}")
        if i.get("type") not in TYPES:
            errors.append(f"{iid}: bad type {i.get('type')}")
        if i.get("priority") not in PRIORITIES:
            errors.append(f"{iid}: bad priority {i.get('priority')}")
        if i.get("epic") not in epic_ids:
            errors.append(f"{iid}: unknown epic {i.get('epic')}")
        if i.get("type") == "conditional" and not i.get("trigger"):
            errors.append(f"{iid}: conditional issue needs a trigger")
        if i.get("type") in {"conditional", "optional"} and not i.get("title", "").startswith(
            "[Conditional]" if i["type"] == "conditional" else "[Optional]"
        ):
            errors.append(f"{iid}: {i['type']} issue title must start with its marker")
        for dep in i.get("depends_on", []):
            if dep not in known:
                errors.append(f"{iid}: depends on unknown {dep}")
            if dep == iid:
                errors.append(f"{iid}: depends on itself")
        if len(i.get("acceptance", [])) < 2:
            errors.append(f"{iid}: needs at least two acceptance criteria")
        for crit in i.get("acceptance", []):
            if any(v in crit.lower() for v in VAGUE):
                errors.append(f"{iid}: vague acceptance criterion: {crit!r}")
        sci = i.get("science")
        if (
            i.get("workstream") in SCIENCE_WORKSTREAMS
            and i.get("type") != "decision"
            and not sci
            and not i.get("science_exempt")
        ):
            errors.append(
                f"{iid}: scientific workstream issue needs a science block or science_exempt reason"
            )
        if sci:
            for k in SCIENCE_KEYS:
                if not sci.get(k):
                    errors.append(f"{iid}: science block missing {k}")
        if i.get("workstream") in UI_WORKSTREAMS and not i.get("design_refs"):
            errors.append(f"{iid}: frontend issue must reference DESIGN.md sections (design_refs)")
    by_id = {i["id"]: i for i in issues}
    for i in issues:
        if i.get("type") in {"task", "decision"}:
            for dep in i.get("depends_on", []):
                if by_id.get(dep, {}).get("type") == "optional":
                    errors.append(f"{i['id']}: required issue depends on optional {dep}")
    try:
        list(TopologicalSorter({i["id"]: i.get("depends_on", []) for i in issues}).static_order())
    except CycleError as exc:
        errors.append(f"dependency cycle: {exc.args[1]}")
    return errors


def status_of(i: dict[str, Any], by_id: dict[str, dict[str, Any]], st: dict[str, Any]) -> str:
    if i["id"] in st["closed"]:
        return "closed"
    deps_open = [d for d in i["depends_on"] if d not in st["closed"]]
    if i["type"] == "conditional" and st["triggered"].get(i["id"]) is not True:
        return "conditional-pending" if deps_open else "conditional-decide"
    if i["type"] == "optional":
        return "optional-blocked" if deps_open else "optional-ready"
    return "blocked" if deps_open else "ready"


def critical_path(issues: list[dict[str, Any]]) -> list[str]:
    """Longest chain of required (task/decision) issues ending at KS-DEL-01."""
    req = {i["id"]: i for i in issues if i["type"] in {"task", "decision"}}
    order = list(
        TopologicalSorter(
            {k: [d for d in v["depends_on"] if d in req] for k, v in req.items()}
        ).static_order()
    )
    best: dict[str, tuple[int, list[str]]] = {}
    for iid in order:
        prev = [best[d] for d in req[iid]["depends_on"] if d in best]
        length, path = max(prev, key=lambda p: p[0]) if prev else (0, [])
        best[iid] = (length + 1, [*path, iid])
    return best.get("KS-DEL-01", max(best.values()))[1]


def bullet(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items) if items else "- None"


def render_issue(
    i: dict[str, Any], by_id: dict[str, dict[str, Any]], status: str, dependents: list[str]
) -> str:
    deps = (
        "\n".join(f"- Blocked by: `{d}` — {by_id[d]['title']}" for d in i["depends_on"])
        or "- None — can start now."
    )
    blocks = "\n".join(f"- Blocks: `{d}` — {by_id[d]['title']}" for d in dependents) or "- None."
    parts = [
        f"<!-- {i['id']} | generated from docs/issues/src/{i['_source']} by scripts/backlog.py; edit the source, not this file -->",
        f"# {i['id']}: {i['title']}",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Type | {i['type']} |",
        f"| Priority | {i['priority']} |",
        f"| Epic | `{i['epic']}` |",
        f"| Workstream | {i['workstream']} |",
        f"| Recommended owner role | {i['owner_role']} |",
        f"| Status (from state.json) | {status} |",
    ]
    if i.get("trigger"):
        parts += ["", f"> **Trigger condition:** {i['trigger']}"]
    parts += [
        "",
        "## Problem",
        "",
        i["problem"].strip(),
        "",
        "## Expected outcome",
        "",
        i["outcome"].strip(),
        "",
        "## Dependencies",
        "",
        deps,
        "",
        blocks,
        "",
        "## Scope",
        "",
        bullet(i["scope"]),
    ]
    parts += ["", "## Explicit exclusions", "", bullet(i.get("exclusions", []))]
    parts += [
        "",
        "## Implementation guidance",
        "",
        i["guidance"].strip(),
        "",
        "## Relevant files and modules",
        "",
        bullet([f"`{f}`" for f in i["files"]]),
        "",
        "## Contract impact",
        "",
        i["contract_impact"],
    ]
    if i.get("design_refs"):
        parts += [
            "",
            "## Design references",
            "",
            bullet(i["design_refs"]),
            "",
            "Interface work must implement the referenced DESIGN.md states exactly; "
            "if the spec must change, update DESIGN.md in the same PR.",
        ]
    if i.get("science"):
        s = i["science"]
        parts += [
            "",
            "## Scientific requirements",
            "",
            f"- **Dataset and label provenance:** {s['dataset']}",
            f"- **Evaluation partition:** {s['partition']}",
            f"- **Applicable metrics:** {s['metrics']}",
            f"- **What cannot be claimed:** {s['cannot_claim']}",
            f"- **Reproducibility artifacts:** {s['artifacts']}",
        ]
    parts += [
        "",
        "## Acceptance criteria",
        "",
        "\n".join(f"- [ ] {a}" for a in i["acceptance"]),
        "",
        "## Verification",
        "",
        bullet([f"`{v}`" if not v[0].isupper() else v for v in i["verification"]]),
        "",
        "## Documentation updates",
        "",
        bullet(i["docs"]),
        "",
        "## Definition of done",
        "",
        bullet(i["dod"] + COMMON_DOD),
        "",
    ]
    return "\n".join(parts)


def render_epic(e: dict[str, Any], children: list[dict[str, Any]], statuses: dict[str, str]) -> str:
    rows = "\n".join(
        f"| `{c['id']}` | {c['title']} | {c['type']} | {c['priority']} | {statuses[c['id']]} |"
        for c in children
    )
    return "\n".join(
        [
            f"<!-- {e['id']} | generated by scripts/backlog.py -->",
            f"# {e['id']}: {e['title']}",
            "",
            e["summary"],
            "",
            "Done when every required child issue is closed with evidence and conditional children are either "
            "closed or recorded as not triggered.",
            "",
            "| Issue | Title | Type | Priority | Status |",
            "|---|---|---|---|---|",
            rows,
            "",
        ]
    )


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    epics, issues = load()
    errors = validate(epics, issues)
    if errors:
        print("backlog: FAIL")
        for e in errors:
            print(f"  {e}")
        return 1
    st = state()
    by_id = {i["id"]: i for i in issues}
    statuses = {i["id"]: status_of(i, by_id, st) for i in issues}
    dependents = {i["id"]: [j["id"] for j in issues if i["id"] in j["depends_on"]] for i in issues}
    if cmd == "check":
        print(f"backlog: ok ({len(epics)} epics, {len(issues)} issues, acyclic)")
        return 0
    if cmd == "ready":
        for i in issues:
            if statuses[i["id"]] in {"ready", "conditional-decide", "optional-ready"}:
                print(f"{i['id']:<14} {statuses[i['id']]:<20} {i['priority']} {i['title']}")
        return 0
    if cmd != "render":
        print(__doc__)
        return 2
    for old in OUT.glob("KS-*.md"):
        old.unlink()
    for i in issues:
        (OUT / f"{i['id']}.md").write_text(
            render_issue(i, by_id, statuses[i["id"]], dependents[i["id"]]), encoding="utf-8"
        )
    for e in epics:
        children = [i for i in issues if i["epic"] == e["id"]]
        (OUT / f"{e['id']}.md").write_text(render_epic(e, children, statuses), encoding="utf-8")
    cp = critical_path(issues)
    manifest = {
        "generated_by": "scripts/backlog.py",
        "epics": [{"id": e["id"], "title": e["title"], "file": f"docs/issues/{e['id']}.md"} for e in epics],
        "issues": [
            {
                "id": i["id"],
                "title": i["title"],
                "epic": i["epic"],
                "type": i["type"],
                "priority": i["priority"],
                "workstream": i["workstream"],
                "owner_role": i["owner_role"],
                "depends_on": i["depends_on"],
                "blocks": dependents[i["id"]],
                "status": statuses[i["id"]],
                "file": f"docs/issues/{i['id']}.md",
            }
            for i in issues
        ],
        "critical_path": cp,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    lines = [
        "<!-- generated by scripts/backlog.py; edit docs/issues/src/*.toml -->",
        "# Backlog manifest",
        "",
        f"{len(issues)} issues in {len(epics)} epics. Status comes from `docs/issues/state.json`.",
        "",
        "| ID | Title | Type | Pri | Workstream | Depends on | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for i in issues:
        deps = ", ".join(f"[{d}]({d}.md)" for d in i["depends_on"]) or "—"
        lines.append(
            f"| [{i['id']}]({i['id']}.md) | {i['title']} | {i['type']} | {i['priority']} | "
            f"{i['workstream']} | {deps} | {statuses[i['id']]} |"
        )
    lines += ["", "## Critical path (required issues)", "", " → ".join(f"`{x}`" for x in cp), ""]
    (OUT / "manifest.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"backlog: rendered {len(issues)} issues + {len(epics)} epics; critical path length {len(cp)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
