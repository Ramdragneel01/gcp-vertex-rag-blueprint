terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.40.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 5.40.0"
    }
  }
}

locals {
  labels = {
    project = "gcp-vertex-rag-blueprint"
    env     = var.environment
  }
}

resource "google_project_service" "required_apis" {
  for_each = toset([
    "aiplatform.googleapis.com",
    "discoveryengine.googleapis.com",
    "storage.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "secretmanager.googleapis.com"
  ])

  project = var.project_id
  service = each.value
}

resource "google_storage_bucket" "rag_docs" {
  name                        = var.bucket_name
  project                     = var.project_id
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true
  labels                      = local.labels

  depends_on = [google_project_service.required_apis]
}

resource "google_service_account" "rag_runtime" {
  project      = var.project_id
  account_id   = "rag-runtime-${var.environment}"
  display_name = "RAG Runtime (${var.environment})"
}

resource "google_project_iam_member" "runtime_vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.rag_runtime.email}"
}

resource "google_project_iam_member" "runtime_discovery_user" {
  project = var.project_id
  role    = "roles/discoveryengine.editor"
  member  = "serviceAccount:${google_service_account.rag_runtime.email}"
}

resource "google_project_iam_member" "runtime_storage_reader" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.rag_runtime.email}"
}

resource "google_discovery_engine_data_store" "rag_store" {
  provider      = google-beta
  project       = var.project_id
  location      = "global"
  data_store_id = var.data_store_id
  display_name  = "RAG Datastore (${var.environment})"
  industry_vertical = "GENERIC"
  content_config    = "CONTENT_REQUIRED"

  depends_on = [google_project_service.required_apis]
}
