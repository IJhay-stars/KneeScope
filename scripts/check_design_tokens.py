"""Check DESIGN.md colour tokens: WCAG contrast pairs and the no-blue/no-purple hue rule.

Reads tokens from web/src/styles/tokens.css if present, otherwise from the TOKENS table
below (kept identical to DESIGN.md section 4). Exit code 1 on any failure.
"""

from __future__ import annotations

import colorsys
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOKENS = {
    # Lightbox (dark workspace)
    "lb-bg": "#191714",
    "lb-panel": "#211F1B",
    "lb-raised": "#2A2722",
    "lb-line": "#3A362F",
    "lb-line-strong": "#746C5E",
    "lb-text": "#EDE7DA",
    "lb-text-muted": "#B9B1A1",
    "lb-text-faint": "#958C7C",
    "lb-accent": "#AEB27A",
    "lb-accent-strong": "#C3C690",
    "lb-on-accent": "#16150F",
    "lb-cached": "#D2AE5E",
    "lb-failed": "#D9805B",
    "lb-focus": "#E6C98A",
    "viewer-well": "#0D0D0D",
    "viewer-text": "#D9D9D9",
    # Ledger (paper documents)
    "lg-paper": "#EFE9DC",
    "lg-paper-2": "#E5DDCB",
    "lg-line": "#C9BEA6",
    "lg-ink": "#1E1B16",
    "lg-ink-muted": "#575043",
    "lg-accent": "#555A2A",
    "lg-failed": "#93421F",
    "lg-cached": "#7A5A12",
}

PAIRS = [
    # (foreground, background, minimum ratio, purpose)
    ("lb-text", "lb-bg", 7.0, "body text on app background"),
    ("lb-text", "lb-panel", 7.0, "body text on panels"),
    ("lb-text-muted", "lb-panel", 4.5, "secondary text on panels"),
    ("lb-text-muted", "lb-raised", 4.5, "secondary text on hover rows"),
    ("lb-text-faint", "lb-panel", 4.5, "tertiary text on panels"),
    ("lb-text-faint", "lb-bg", 4.5, "tertiary text on background"),
    ("lb-accent", "lb-panel", 4.5, "accent text/links on panels"),
    ("lb-on-accent", "lb-accent", 7.0, "primary button label"),
    ("lb-cached", "lb-panel", 4.5, "cached badge text"),
    ("lb-failed", "lb-panel", 4.5, "failed/error text"),
    ("lb-focus", "lb-panel", 3.0, "focus ring (non-text)"),
    ("lb-focus", "lb-bg", 3.0, "focus ring on background (non-text)"),
    ("lb-line-strong", "lb-panel", 3.0, "control and input borders (WCAG 1.4.11)"),
    ("viewer-text", "viewer-well", 7.0, "viewer overlay text"),
    ("lg-ink", "lg-paper", 7.0, "ledger body text"),
    ("lg-ink-muted", "lg-paper", 4.5, "ledger secondary text"),
    ("lg-ink-muted", "lg-paper-2", 4.5, "ledger secondary text on table stripe"),
    ("lg-accent", "lg-paper", 4.5, "ledger accent"),
    ("lg-failed", "lg-paper", 4.5, "ledger failure text"),
    ("lg-cached", "lg-paper", 4.5, "ledger cached text"),
]

# Hues (degrees) considered blue, cyan-blue, or purple. Any token with meaningful
# saturation inside this band fails.
FORBIDDEN_HUE = (170.0, 330.0)
SATURATION_FLOOR = 0.12


def hex_to_rgb(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def luminance(rgb: tuple[float, float, float]) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = luminance(hex_to_rgb(a)), luminance(hex_to_rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def load_tokens() -> dict[str, str]:
    css = ROOT / "web" / "src" / "styles" / "tokens.css"
    if not css.exists():
        return dict(TOKENS)
    found = dict(re.findall(r"--ks-([a-z0-9-]+):\s*(#[0-9A-Fa-f]{6})", css.read_text()))
    missing = sorted(set(TOKENS) - set(found))
    if missing:
        print(f"tokens.css is missing DESIGN.md tokens: {missing}")
        sys.exit(1)
    drift = {k: (found[k], TOKENS[k]) for k in TOKENS if found[k].upper() != TOKENS[k].upper()}
    if drift:
        print(f"tokens.css drifts from DESIGN.md: {drift}")
        sys.exit(1)
    return found


def main() -> int:
    tokens = load_tokens()
    failures = 0
    for fg, bg, minimum, purpose in PAIRS:
        ratio = contrast(tokens[fg], tokens[bg])
        ok = ratio >= minimum
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {ratio:5.2f} >= {minimum:<4} {fg} on {bg} ({purpose})")
    for name, value in tokens.items():
        h, _l, s = colorsys.rgb_to_hls(*hex_to_rgb(value))
        hue = h * 360
        if s >= SATURATION_FLOOR and FORBIDDEN_HUE[0] <= hue <= FORBIDDEN_HUE[1]:
            failures += 1
            print(f"FAIL hue {hue:5.1f} sat {s:.2f} {name} {value} is in the blue/purple band")
    print("design tokens:", "FAIL" if failures else "ok")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
