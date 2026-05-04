# Runbook

## Service

- default port: 8093
- health: GET /health
- readiness: GET /ready
- metrics: GET /metrics

## Local Operations

```bash
pip install -r requirements-dev.txt
pip install -e .
python -m gcp_vertex_rag_blueprint
```

## Smoke Checks

```bash
curl http://localhost:8093/health
curl http://localhost:8093/ready
curl http://localhost:8093/v1/config
```

## Terraform Operations

```bash
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```

## Incident Playbooks

### Retrieval endpoint returns low-quality context

1. Verify datastore indexing status in Discovery Engine.
2. Confirm `GVRB_VERTEX_DATA_STORE_ID` matches deployed datastore.
3. Lower or raise `retrieval_top_k` and re-evaluate.

### API returns failures after backend switch

1. Validate service account roles (`aiplatform.user`, `discoveryengine.editor`).
2. Validate project/location settings.
3. Fall back to mock backend to isolate infra vs app causes.

### Elevated latency

1. Check p95 for retrieval and generation in metrics stack.
2. Tune top-k and prompt size.
3. Ensure region alignment between service and Vertex resources.
