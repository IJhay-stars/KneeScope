"""Contract rules that make states and provenance distinguishable."""

import json
from datetime import UTC, datetime
from pathlib import Path

import jsonschema
import pytest
from pydantic import ValidationError

from kneescope_contracts.findings import load_profile, profile_ids
from kneescope_contracts.models import (
    FindingMetrics,
    FindingResult,
    MetricsSnapshot,
    MetricValue,
    ResultProvenance,
    StudyDetail,
)

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 13, tzinfo=UTC)


def test_every_profile_resolves():
    for pid in profile_ids():
        assert load_profile(pid).findings


def test_mrnet_profile_has_no_invented_labels():
    ids = {f.finding_id for f in load_profile("mrnet3").findings}
    assert ids == {"abnormal", "acl_tear", "meniscal_tear"}


def test_low_score_is_still_scored():
    r = FindingResult(
        finding_id="acl",
        display_name="ACL",
        status="scored",
        score=0.02,
        score_kind="uncalibrated_model_score",
    )
    assert r.status == "scored"


@pytest.mark.parametrize("status", ["unavailable", "unsupported", "failed"])
def test_non_scored_states_need_reason_and_no_score(status):
    with pytest.raises(ValidationError):
        FindingResult(finding_id="acl", display_name="ACL", status=status)
    with pytest.raises(ValidationError):
        FindingResult(
            finding_id="acl",
            display_name="ACL",
            status=status,
            score=0.5,
            reason={"code": "X", "message": "y"},
        )


def test_threshold_consistency():
    with pytest.raises(ValidationError):
        FindingResult(
            finding_id="acl",
            display_name="ACL",
            status="scored",
            score=0.2,
            score_kind="uncalibrated_model_score",
            threshold=0.5,
            above_threshold=True,
        )


def test_cached_cannot_claim_live_latency():
    with pytest.raises(ValidationError):
        ResultProvenance(source="cached", computed_at=NOW, served_at=NOW, cache_key="k", latency_ms=12.0)


def test_live_requires_latency():
    with pytest.raises(ValidationError):
        ResultProvenance(source="live", computed_at=NOW, served_at=NOW)


def test_fixture_requires_fixture_notice():
    with pytest.raises(ValidationError):
        ResultProvenance(source="fixture", computed_at=None, served_at=NOW, notice="demo")


def test_single_class_auc_cannot_be_defined():
    undefined = MetricValue(status="not_computed", reason="n/a")
    with pytest.raises(ValidationError):
        FindingMetrics(
            finding_id="mcl",
            n_positive=0,
            n_negative=40,
            n_unknown=3,
            roc_auc=MetricValue(value=0.5, status="defined"),
            pr_auc=undefined,
            sensitivity=undefined,
            specificity=undefined,
            brier=undefined,
        )


def test_fixture_metrics_can_only_be_unavailable():
    with pytest.raises(ValidationError):
        MetricsSnapshot(status="available", origin="fixture")


def test_fixtures_validate():
    data = json.loads((ROOT / "contracts/fixtures/studies.json").read_text())
    for s in data["studies"]:
        StudyDetail.model_validate(s)
    MetricsSnapshot.model_validate_json((ROOT / "contracts/fixtures/metrics.json").read_text())


def test_examples_match_exported_json_schema():
    pairs = {
        "studies": "StudyList",
        "study-detail": "StudyDetail",
        "prediction-fixture": "PredictionResponse",
        "prediction-missing-plane": "PredictionResponse",
        "explanation-available": "Explanation",
        "explanation-unavailable": "Explanation",
        "labels": "StudyLabels",
        "metrics-unavailable": "MetricsSnapshot",
        "model-card": "ModelCard",
        "health": "Health",
        "error-preprocessing-failed": "ApiError",
        "error-study-not-found": "ApiError",
    }
    for example, schema in pairs.items():
        body = json.loads((ROOT / f"contracts/examples/{example}.json").read_text())["body"]
        body = json.loads(json.dumps(body).replace('"<volatile>"', '"2026-10-13T00:00:00Z"'))
        jsonschema.validate(body, json.loads((ROOT / f"contracts/schema/{schema}.schema.json").read_text()))
