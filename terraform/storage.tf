resource "google_storage_bucket" "access_logs" {
  #checkov:skip=CKV_GCP_62:This bucket is the dedicated destination for GCS access logs; enabling recursive logging is not useful.
  name                        = "${var.bucket_name}-access-logs"
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 365
    }

    action {
      type = "Delete"
    }
  }

  labels = {
    environment = var.environment
    data_zone   = "security-logs"
  }
}

resource "google_storage_bucket" "raw_landing" {
  #checkov:skip=CKV_GCP_62:The raw bucket sends access logs to the dedicated security-log bucket below.
  name                        = var.bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  logging {
    log_bucket = google_storage_bucket.access_logs.name
  }

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
