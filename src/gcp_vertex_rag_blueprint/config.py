"""Application settings using GVRB_ environment variables."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GVRB_", env_file=".env", extra="ignore")

    service_name: str = "gcp-vertex-rag-blueprint"
    host: str = "0.0.0.0"
    port: int = 8093
    log_level: str = "INFO"

    gcp_project_id: str = "demo-project"
    gcp_location: str = "us-central1"
    vertex_data_store_id: str = "sample-datastore"
    rag_corpus_name: str = "knowledge-corpus"

    model_name: str = "gemini-1.5-pro"
    retrieval_top_k: int = Field(5, ge=1, le=20)
    enable_mock_backends: bool = True

    request_timeout_seconds: float = Field(8.0, ge=0.5, le=60.0)
