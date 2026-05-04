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

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

module "rag_stack" {
  source       = "../../modules/rag_stack"
  project_id   = var.project_id
  region       = var.region
  environment  = "dev"
  bucket_name  = var.bucket_name
  data_store_id = var.data_store_id
}
