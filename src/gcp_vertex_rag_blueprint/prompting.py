"""Prompt construction for grounded answer generation."""
from __future__ import annotations

from .models import RetrievedChunk


def build_grounded_prompt(query: str, chunks: list[RetrievedChunk]) -> str:
    numbered_context = "\n".join(
        f"[{i + 1}] {chunk.title} :: {chunk.text}" for i, chunk in enumerate(chunks)
    )
    return (
        "You are a production assistant. Use ONLY the provided context to answer.\n"
        "If context is insufficient, say so clearly and do not fabricate.\n\n"
        f"Question:\n{query}\n\n"
        f"Context:\n{numbered_context}\n\n"
        "Return: concise answer + bullet list of cited source numbers."
    )
