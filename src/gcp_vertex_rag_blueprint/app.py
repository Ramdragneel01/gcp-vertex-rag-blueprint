"""FastAPI surface for the Vertex RAG blueprint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import Response

from .config import Settings
from .generator import GeminiGenerator, MockGenerator
from .metrics import export_metrics, mark_request
from .models import AnswerRequest, AnswerResponse, HealthResponse, RetrieveRequest, RetrieveResponse
from .pipeline import RagPipeline
from .retriever import MockRetriever, VertexSearchRetriever


def _build_pipeline(settings: Settings) -> RagPipeline:
    if settings.enable_mock_backends:
        retriever = MockRetriever(data_store_id=settings.vertex_data_store_id)
        generator = MockGenerator(model_name=settings.model_name)
        return RagPipeline(retriever=retriever, generator=generator, backend_name="mock")

    retriever = VertexSearchRetriever(
        project_id=settings.gcp_project_id,
        location=settings.gcp_location,
        data_store_id=settings.vertex_data_store_id,
    )
    generator = GeminiGenerator(
        model_name=settings.model_name,
        project_id=settings.gcp_project_id,
        location=settings.gcp_location,
    )
    return RagPipeline(retriever=retriever, generator=generator, backend_name="vertex")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    pipeline = _build_pipeline(settings)

    app = FastAPI(title="gcp-vertex-rag-blueprint", version="0.1.0")

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", service=settings.service_name)

    @app.get("/ready", response_model=HealthResponse)
    def ready() -> HealthResponse:
        return HealthResponse(status="ready", service=settings.service_name)

    @app.get("/metrics")
    def metrics() -> Response:
        payload, content_type = export_metrics()
        return Response(content=payload, media_type=content_type)

    @app.get("/v1/config")
    def config() -> dict:
        return {
            "project": settings.gcp_project_id,
            "location": settings.gcp_location,
            "data_store": settings.vertex_data_store_id,
            "model": settings.model_name,
            "backend": pipeline.backend_name,
        }

    @app.post("/v1/retrieve", response_model=RetrieveResponse)
    def retrieve(payload: RetrieveRequest) -> RetrieveResponse:
        mark_request(endpoint="retrieve", backend=pipeline.backend_name)
        top_k = payload.top_k or settings.retrieval_top_k
        return pipeline.retrieve(query=payload.query, top_k=top_k)

    @app.post("/v1/answer", response_model=AnswerResponse)
    def answer(payload: AnswerRequest) -> AnswerResponse:
        mark_request(endpoint="answer", backend=pipeline.backend_name)
        top_k = payload.top_k or settings.retrieval_top_k
        return pipeline.answer(query=payload.query, top_k=top_k, include_sources=payload.include_sources)

    return app


app = create_app()
