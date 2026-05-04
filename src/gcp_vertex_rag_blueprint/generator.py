"""Answer generation abstraction for Gemini-backed grounded answers."""
from __future__ import annotations

from dataclasses import dataclass


class Generator:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


@dataclass
class MockGenerator(Generator):
    model_name: str

    def generate(self, prompt: str) -> str:
        excerpt = prompt.strip().replace("\n", " ")[:180]
        return (
            f"[{self.model_name}] Grounded answer draft. "
            f"Prompt excerpt: {excerpt} ..."
        )


@dataclass
class GeminiGenerator(Generator):
    model_name: str
    project_id: str
    location: str

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "Real Gemini integration is intentionally omitted in this local blueprint. "
            "Wire Vertex AI SDK calls here for production deployment."
        )
