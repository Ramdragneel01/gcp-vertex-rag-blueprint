"""Retrieval layer abstraction for Vertex AI Search backed RAG."""
from __future__ import annotations

from dataclasses import dataclass

from .models import RetrievedChunk


class Retriever:
    def retrieve(self, query: str, top_k: int) -> list[RetrievedChunk]:
        raise NotImplementedError


@dataclass
class MockRetriever(Retriever):
    data_store_id: str

    def retrieve(self, query: str, top_k: int) -> list[RetrievedChunk]:
        query_short = query.strip()[:60]
        return [
            RetrievedChunk(
                id=f"doc-{i + 1}",
                title=f"Mock Knowledge Doc {i + 1}",
                text=f"Relevant context for '{query_short}' from datastore {self.data_store_id}.",
                source_uri=f"gs://vertex-rag-sample/doc-{i + 1}.md",
                score=max(0.0, 0.95 - i * 0.08),
            )
            for i in range(top_k)
        ]


@dataclass
class VertexSearchRetriever(Retriever):
    project_id: str
    location: str
    data_store_id: str

    def retrieve(self, query: str, top_k: int) -> list[RetrievedChunk]:
        raise NotImplementedError(
            "Real Vertex AI Search integration is intentionally omitted in this local blueprint. "
            "Wire google-cloud-discoveryengine client here for production deployment."
        )
