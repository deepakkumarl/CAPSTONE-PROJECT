# Minimal Terraform Configuration Placeholder
# Demonstrates cloud infrastructure provisioning layout for future deployment.

terraform {
  required_version = ">= 1.3.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

provider "local" {}

# Example local file resource documenting deployment configuration
resource "local_file" "backend_config" {
  filename = "${path.module}/backend_deployment_manifest.json"
  content  = jsonencode({
    project     = "bmw-service-knowledge-rag"
    environment = "development"
    services    = {
      fastapi_backend = {
        port = 8000
        env  = "OLLAMA_BASE_URL=http://localhost:11434"
      }
      streamlit_ui = {
        port = 8501
      }
    }
  })
}

output "deployment_status" {
  value = "Local capstone infrastructure manifest generated at ${local_file.backend_config.filename}"
}
