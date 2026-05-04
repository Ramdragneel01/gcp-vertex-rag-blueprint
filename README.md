# gcp-vertex-rag-blueprint

Production-first reference blueprint for building grounded RAG systems on Google Cloud with Vertex AI Search and Gemini.

[![CI](https://github.com/Ramdragneel01/gcp-vertex-rag-blueprint/actions/workflows/ci.yml/badge.svg)](https://github.com/Ramdragneel01/gcp-vertex-rag-blueprint/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Why

Most RAG examples are notebook-grade and stop before infra, runtime hardening, and operational guardrails. This blueprint includes:

- FastAPI service with retrieval and answer endpoints
- mock/vertex backend abstraction for local-to-cloud progression
- Terraform module for core GCP RAG stack
- CI pipeline for lint/tests/terraform validate/container smoke
- health/readiness/metrics and runbook docs

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) and [docs/assets/architecture.mmd](docs/assets/architecture.mmd).

## Quick Start (Local)

```bash
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements-dev.txt
pip install -e .
python -m gcp_vertex_rag_blueprint
```

Test locally:

```bash
curl http://localhost:8093/health
curl http://localhost:8093/v1/config
curl -X POST http://localhost:8093/v1/retrieve -H "content-type: application/json" -d "{\"query\":\"How to rotate API keys safely?\"}"
curl -X POST http://localhost:8093/v1/answer -H "content-type: application/json" -d "{\"query\":\"How to rotate API keys safely?\"}"
```

## Docker

```bash
docker compose up --build
```

Service URL: http://localhost:8093

## Terraform (Dev)

```bash
cd terraform/environments/dev
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

## API Endpoints

- GET /health
- GET /ready
- GET /metrics
- GET /v1/config
- POST /v1/retrieve
- POST /v1/answer

## Testing

```bash
pytest
ruff check src tests
```

Current baseline: 21 passing tests.

## Security and Ops

- Security model: [SECURITY.md](SECURITY.md)
- Operations runbook: [docs/RUNBOOK.md](docs/RUNBOOK.md)

## Roadmap

- Wire real Discovery Engine search client in retriever
- Wire real Gemini generation via Vertex SDK
- Add Cloud Run deployment module and IAM least-privilege refinements
- Add evaluation harness integration for answer faithfulness

## License

MIT
