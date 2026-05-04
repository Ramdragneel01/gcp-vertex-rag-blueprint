from gcp_vertex_rag_blueprint.config import Settings


def test_default_settings():
    s = Settings()
    assert s.service_name == "gcp-vertex-rag-blueprint"
    assert s.retrieval_top_k == 5
    assert s.enable_mock_backends is True


def test_custom_settings():
    s = Settings(gcp_project_id="acme-prod", retrieval_top_k=7, enable_mock_backends=False)
    assert s.gcp_project_id == "acme-prod"
    assert s.retrieval_top_k == 7
    assert s.enable_mock_backends is False
