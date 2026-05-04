# Architecture

## Objective

Provide a production-oriented baseline for grounded RAG on GCP that bridges local developer workflows and cloud deployment.

## Components

- API service (`src/gcp_vertex_rag_blueprint/app.py`)
  - `/v1/retrieve` and `/v1/answer` endpoints
  - health, readiness, and Prometheus metrics
- Pipeline (`pipeline.py`)
  - retrieve -> prompt -> generate flow
- Retrieval abstraction (`retriever.py`)
  - `MockRetriever` for local test
  - `VertexSearchRetriever` contract for cloud integration
- Generator abstraction (`generator.py`)
  - `MockGenerator` for local test
  - `GeminiGenerator` contract for cloud integration
- IaC (`terraform/modules/rag_stack`)
  - APIs, bucket, service account, IAM, Vertex Search datastore

## Request Flow

1. Client submits query to `/v1/answer`.
2. Retriever fetches top-k chunks from configured backend.
3. Prompting layer builds grounded prompt with numbered evidence.
4. Generator returns grounded response draft.
5. Response includes sources for auditability.

## Deployment Topology

Mermaid source is in `docs/assets/architecture.mmd`.

- Cloud Run service hosts API.
- Discovery Engine datastore serves retrieval.
- GCS bucket stores indexed source corpora.
- Service account provides least-privilege runtime identity.

## Design Decisions

- Mock-first backend strategy keeps local development deterministic.
- Explicit backend interfaces isolate cloud SDK coupling.
- Terraform module isolates infra concerns from app runtime logic.
