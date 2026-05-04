output "bucket_name" {
  value       = google_storage_bucket.rag_docs.name
  description = "Bucket that stores RAG source documents"
}

output "runtime_service_account" {
  value       = google_service_account.rag_runtime.email
  description = "Runtime service account used by API services"
}

output "data_store_id" {
  value       = google_discovery_engine_data_store.rag_store.data_store_id
  description = "Vertex AI Search datastore id"
}
