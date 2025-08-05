variable "databricks_host" {
  description = "The Databricks workspace URL"
  type        = string
  sensitive   = true
}

variable "databricks_token" {
  description = "The Databricks personal access token"
  type        = string
  sensitive   = true
}
