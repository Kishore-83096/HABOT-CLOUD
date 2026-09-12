resource "google_storage_bucket" "raw_landing" {
  name                        = var.bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }

    action {
      type = "Delete"
    }
  }

  labels = {
    environment = var.environment
    data_zone   = "d0-raw"
  }
}
