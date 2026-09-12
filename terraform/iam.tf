resource "google_service_account" "ingestion" {
  account_id   = "student-ingestion-${var.environment}"
  display_name = "Student ingestion service account"
}

resource "google_storage_bucket_iam_member" "ingestion_object_creator" {
  bucket = google_storage_bucket.raw_landing.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.ingestion.email}"
}

resource "google_project_iam_member" "ingestion_bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.ingestion.email}"
}

resource "google_bigquery_dataset_iam_member" "ingestion_data_editor" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.staged.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.ingestion.email}"
}
