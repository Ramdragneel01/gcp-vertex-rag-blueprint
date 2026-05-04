import pytest

from gcp_vertex_rag_blueprint.generator import GeminiGenerator, MockGenerator
from gcp_vertex_rag_blueprint.retriever import MockRetriever, VertexSearchRetriever


def test_mock_retriever_top_k():
    retriever = MockRetriever(data_store_id="ds-1")
    chunks = retriever.retrieve("How to deploy", top_k=3)
    assert len(chunks) == 3
    assert all(c.source_uri.startswith("gs://") for c in chunks)


def test_mock_retriever_scores_descend():
    retriever = MockRetriever(data_store_id="ds-1")
    chunks = retriever.retrieve("How to deploy", top_k=4)
    assert chunks[0].score > chunks[1].score > chunks[2].score


def test_mock_generator_includes_model_name():
    g = MockGenerator(model_name="gemini-1.5-pro")
    out = g.generate("hello")
    assert "gemini-1.5-pro" in out


def test_vertex_retriever_not_implemented():
    retriever = VertexSearchRetriever(project_id="p", location="us", data_store_id="d")
    with pytest.raises(NotImplementedError):
        retriever.retrieve("x", 3)


def test_gemini_generator_not_implemented():
    g = GeminiGenerator(model_name="gemini-1.5-pro", project_id="p", location="us")
    with pytest.raises(NotImplementedError):
        g.generate("prompt")
