variable "project_id" {
  type        = string
  description = "GCP project id"
}

variable "region" {
  type        = string
  description = "Primary GCP region"
  default     = "us-central1"
}

variable "bucket_name" {
  type        = string
  description = "Bucket name for RAG source docs"
}

variable "data_store_id" {
  type        = string
  description = "Vertex AI Search datastore id"
  default     = "vertex-rag-datastore-dev"
}
