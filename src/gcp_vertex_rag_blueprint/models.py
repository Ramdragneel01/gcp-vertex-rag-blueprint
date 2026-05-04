"""Pydantic request/response contracts for the API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    id: str
    title: str
    text: str
    source_uri: str
    score: float = Field(ge=0.0, le=1.0)


class RetrieveRequest(BaseModel):
    query: str = Field(min_length=2, max_length=4000)
    top_k: int | None = Field(default=None, ge=1, le=20)


class RetrieveResponse(BaseModel):
    query: str
    chunks: list[RetrievedChunk]
    backend: str


class AnswerRequest(BaseModel):
    query: str = Field(min_length=2, max_length=4000)
    top_k: int | None = Field(default=None, ge=1, le=20)
    include_sources: bool = True


class AnswerResponse(BaseModel):
    query: str
    answer: str
    sources: list[str]
    backend: str


class HealthResponse(BaseModel):
    status: str
    service: str
