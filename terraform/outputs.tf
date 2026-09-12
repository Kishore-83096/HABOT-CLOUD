output "raw_bucket_name" {
  description = "D0 raw landing bucket name."
  value       = google_storage_bucket.raw_landing.name
}

output "staged_dataset_id" {
  description = "D1 staged BigQuery dataset ID."
  value       = google_bigquery_dataset.staged.dataset_id
}

output "ingestion_service_account" {
  description = "Service account used by the ingestion path."
  value       = google_service_account.ingestion.email
}
