"""Prometheus counters for request-level observability."""
from __future__ import annotations

from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

REQUESTS = Counter("gvrb_requests_total", "Total API requests", ["endpoint", "backend"])


def mark_request(endpoint: str, backend: str) -> None:
    REQUESTS.labels(endpoint=endpoint, backend=backend).inc()


def export_metrics() -> tuple[bytes, str]:
    return generate_latest(), CONTENT_TYPE_LATEST
