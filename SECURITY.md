# Security Policy

## Reporting

Please report vulnerabilities privately:

- ramprakashdhulipudi@gmail.com

Do not disclose security issues publicly before remediation.

## Threat Model (v0.1)

In scope:
- prompt injection attempts through user query input
- unauthorized data exposure from retrieval responses
- over-privileged runtime service account on GCP
- secret/key leakage through local env files

Out of scope:
- tenant-level RBAC (single-tenant blueprint)
- advanced red-team prompt defense automation

## Baseline Controls

- grounded prompt instructs strict context-only answering
- explicit source URIs included for answer traceability
- service account roles are explicitly scoped in Terraform
- `.env` files ignored by git
- health/readiness/metrics endpoints available for monitoring

## Hardening Recommendations

- add API auth in front of `/v1/*` endpoints (IAP, gateway, or JWT)
- enforce WAF and request quotas for abuse prevention
- add content safety filters before generation
- rotate service account credentials and enable CMEK where required
