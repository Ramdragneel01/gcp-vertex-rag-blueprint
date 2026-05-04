variable "project_id" {
  type        = string
  description = "GCP project id"
}

variable "region" {
  type        = string
  description = "Primary region"
  default     = "us-central1"
}

variable "environment" {
  type        = string
  description = "Environment name"
  default     = "dev"
}

variable "bucket_name" {
  type        = string
  description = "Bucket for RAG documents"
}

variable "data_store_id" {
  type        = string
  description = "Vertex AI Search datastore id"
  default     = "vertex-rag-datastore"
}
