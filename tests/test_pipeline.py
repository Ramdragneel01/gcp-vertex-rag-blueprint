from gcp_vertex_rag_blueprint.generator import MockGenerator
from gcp_vertex_rag_blueprint.pipeline import RagPipeline
from gcp_vertex_rag_blueprint.retriever import MockRetriever


def _pipeline():
    return RagPipeline(
        retriever=MockRetriever(data_store_id="sample"),
        generator=MockGenerator(model_name="gemini-1.5-pro"),
        backend_name="mock",
    )


def test_pipeline_retrieve_response():
    p = _pipeline()
    out = p.retrieve(query="How does failover work?", top_k=2)
    assert out.query == "How does failover work?"
    assert out.backend == "mock"
    assert len(out.chunks) == 2


def test_pipeline_answer_includes_sources():
    p = _pipeline()
    out = p.answer(query="How does failover work?", top_k=3, include_sources=True)
    assert out.backend == "mock"
    assert len(out.sources) == 3
    assert "Grounded answer draft" in out.answer


def test_pipeline_answer_without_sources():
    p = _pipeline()
    out = p.answer(query="How does failover work?", top_k=3, include_sources=False)
    assert out.sources == []
