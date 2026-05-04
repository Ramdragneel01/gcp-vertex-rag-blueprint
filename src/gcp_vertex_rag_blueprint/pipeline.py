"""RAG pipeline orchestration (retrieve -> prompt -> generate)."""
from __future__ import annotations

from dataclasses import dataclass

from .generator import Generator
from .models import AnswerResponse, RetrieveResponse
from .prompting import build_grounded_prompt
from .retriever import Retriever


@dataclass
class RagPipeline:
    retriever: Retriever
    generator: Generator
    backend_name: str

    def retrieve(self, query: str, top_k: int) -> RetrieveResponse:
        chunks = self.retriever.retrieve(query=query, top_k=top_k)
        return RetrieveResponse(query=query, chunks=chunks, backend=self.backend_name)

    def answer(self, query: str, top_k: int, include_sources: bool = True) -> AnswerResponse:
        retrieval = self.retrieve(query=query, top_k=top_k)
        prompt = build_grounded_prompt(query=query, chunks=retrieval.chunks)
        answer_text = self.generator.generate(prompt)
        sources = [chunk.source_uri for chunk in retrieval.chunks] if include_sources else []
        return AnswerResponse(
            query=query,
            answer=answer_text,
            sources=sources,
            backend=self.backend_name,
        )
