from gcp_vertex_rag_blueprint.metrics import export_metrics, mark_request


def test_metrics_emit_counter_text():
    mark_request("retrieve", "mock")
    payload, content_type = export_metrics()
    text = payload.decode("utf-8")
    assert "gvrb_requests_total" in text
    assert "retrieve" in text
    assert content_type.startswith("text/plain")
