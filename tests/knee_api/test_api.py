from fastapi.testclient import TestClient

from knee_api.main import app
from kneeml.constants import FINDINGS

client = TestClient(app)


def test_healthz() -> None:
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_predict_returns_every_finding_in_contract_order() -> None:
    r = client.post("/v1/predict", json={"exam_id": "demo-001"})
    assert r.status_code == 200
    body = r.json()
    assert [f["name"] for f in body["findings"]] == FINDINGS
    assert all(0 <= f["probability"] <= 1 for f in body["findings"])
    assert "not for clinical use" in body["disclaimer"].lower()
