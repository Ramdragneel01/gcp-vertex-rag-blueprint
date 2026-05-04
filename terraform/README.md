# Terraform Blueprint

## Layout

- `modules/rag_stack`: reusable infrastructure module
- `environments/dev`: environment wiring and provider setup

## What It Provisions

- Required GCP APIs for Vertex + Discovery Engine + Cloud Run stack
- GCS bucket for source documents
- Runtime service account + minimum baseline IAM
- Vertex AI Search datastore (Discovery Engine)

## Usage

```bash
cd terraform/environments/dev
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

## Notes

- This blueprint intentionally keeps IAM narrow and explicit.
- Expand with VPC, Cloud Run, and Secret Manager bindings for production.
