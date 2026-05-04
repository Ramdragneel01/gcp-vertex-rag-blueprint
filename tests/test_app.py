from fastapi.testclient import TestClient

from gcp_vertex_rag_blueprint.app import create_app
from gcp_vertex_rag_blueprint.config import Settings


def _client() -> TestClient:
    app = create_app(Settings(enable_mock_backends=True, retrieval_top_k=4))
    return TestClient(app)


def test_health_and_ready():
    c = _client()
    h = c.get("/health")
    r = c.get("/ready")
    assert h.status_code == 200
    assert r.status_code == 200
    assert h.json()["status"] == "ok"
    assert r.json()["status"] == "ready"


def test_metrics_endpoint():
    c = _client()
    response = c.get("/metrics")
    assert response.status_code == 200
    assert "gvrb_requests_total" in response.text


def test_config_endpoint():
    c = _client()
    response = c.get("/v1/config")
    assert response.status_code == 200
    body = response.json()
    assert body["backend"] == "mock"
    assert "model" in body


def test_retrieve_endpoint_default_top_k():
    c = _client()
    response = c.post("/v1/retrieve", json={"query": "How to rotate keys?"})
    assert response.status_code == 200
    body = response.json()
    assert body["backend"] == "mock"
    assert len(body["chunks"]) == 4


def test_retrieve_endpoint_override_top_k():
    c = _client()
    response = c.post("/v1/retrieve", json={"query": "How to rotate keys?", "top_k": 2})
    assert response.status_code == 200
    assert len(response.json()["chunks"]) == 2


def test_answer_endpoint_with_sources():
    c = _client()
    response = c.post("/v1/answer", json={"query": "What is our RTO?", "top_k": 3})
    assert response.status_code == 200
    body = response.json()
    assert body["backend"] == "mock"
    assert len(body["sources"]) == 3


def test_answer_endpoint_without_sources():
    c = _client()
    response = c.post("/v1/answer", json={"query": "What is our RTO?", "include_sources": False})
    assert response.status_code == 200
    assert response.json()["sources"] == []


def test_validation_error_for_empty_query():
    c = _client()
    response = c.post("/v1/retrieve", json={"query": ""})
    assert response.status_code == 422
