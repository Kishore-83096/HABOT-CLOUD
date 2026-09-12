variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "Google Cloud region for regional resources."
  type        = string
  default     = "europe-west2"
}

variable "environment" {
  description = "Deployment environment label."
  type        = string
  default     = "dev"
}

variable "bucket_name" {
  description = "Globally unique raw landing bucket name."
  type        = string
}

variable "analyst_group" {
  description = "Google group allowed to read rows that require support."
  type        = string
}
