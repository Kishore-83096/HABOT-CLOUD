resource "google_bigquery_dataset" "staged" {
  dataset_id                 = "student_staged_${var.environment}"
  location                   = var.region
  delete_contents_on_destroy = false

  labels = {
    environment = var.environment
    data_zone   = "d1-staged"
  }
}

resource "google_bigquery_table" "student_onboarding" {
  dataset_id = google_bigquery_dataset.staged.dataset_id
  table_id   = "student_onboarding"

  schema = jsonencode([
    {
      name       = "student_id"
      type       = "STRING"
      mode       = "REQUIRED"
      policyTags = null
    },
    {
      name = "student_name"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "age"
      type = "INTEGER"
      mode = "REQUIRED"
    },
    {
      name = "has_learning_difficulty"
      type = "BOOLEAN"
      mode = "REQUIRED"
    },
    {
      name = "support_required"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "parent_email"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "created_at"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    }
  ])

  time_partitioning {
    type  = "DAY"
    field = "created_at"
  }
}

resource "google_bigquery_row_access_policy" "support_required" {
  project          = var.project_id
  dataset_id       = google_bigquery_dataset.staged.dataset_id
  table_id         = google_bigquery_table.student_onboarding.table_id
  policy_id        = "support-required"
  filter_predicate = "has_learning_difficulty = TRUE"
  grantees         = ["group:${var.analyst_group}"]
}
