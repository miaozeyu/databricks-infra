# Create a serverless SQL endpoint (warehouse)
resource "databricks_sql_endpoint" "serverless_warehouse" {
  name             = "serverless-warehouse"
  cluster_size     = "X-Small"
  max_num_clusters = 1
  auto_stop_mins   = 15

  # Required for serverless
  enable_serverless_compute = true
  warehouse_type            = "PRO"

}

# Create a schema in the first_catalog
resource "databricks_schema" "first_schema" {
  catalog_name = "first_catalog"
  name         = "first_schema"
  comment      = "This is the first schema in the first_catalog"

  # Ensure the schema is created after the warehouse is ready
  depends_on = [databricks_sql_endpoint.serverless_warehouse]
}

# Create a table in the first_schema using the serverless warehouse
resource "databricks_sql_table" "trips_table" {
  catalog_name       = "first_catalog"
  schema_name        = databricks_schema.first_schema.name
  name               = "trips"
  table_type         = "MANAGED"
  data_source_format = "DELTA"

  # Use the serverless warehouse
  warehouse_id = databricks_sql_endpoint.serverless_warehouse.id

  # Schema based on samples.nyctaxi.trips
  column {
    name = "tpep_pickup_datetime"
    type = "TIMESTAMP"
  }
  column {
    name = "tpep_dropoff_datetime"
    type = "TIMESTAMP"
  }
  column {
    name = "trip_distance"
    type = "DOUBLE"
  }
  column {
    name = "fare_amount"
    type = "DOUBLE"
  }
  column {
    name = "pickup_zip"
    type = "INT"
  }
  column {
    name = "dropoff_zip"
    type = "INT"
  }
}

# Create a notebook for the data copy job
resource "databricks_notebook" "copy_nyctaxi_data" {
  source   = "${path.module}/notebooks/copy_nyctaxi_data.sql"
  path     = "/Shared/nyctaxi_data_copy"
  language = "SQL"
}

# Create a job to copy data from samples.nyctaxi.trips to our new table
resource "databricks_job" "nyctaxi_data_copy" {
  name = "NYC Taxi Data Copy"

  # Use the notebook with the copy logic
  task {
    task_key = "copy_nyctaxi_data"
    notebook_task {
      notebook_path = databricks_notebook.copy_nyctaxi_data.path
      source        = "WORKSPACE"
      warehouse_id  = databricks_sql_endpoint.serverless_warehouse.id
    }

    email_notifications {
      on_success = ["miaozeyu@gmail.com"]
      on_failure = ["miaozeyu@gmail.com"]
    }

    max_retries = 1
  }

  # Schedule to run daily at 5 AM
  schedule {
    quartz_cron_expression = "0 0 5 * * ?" # Every day at 5 AM
    timezone_id            = "America/New_York"
    pause_status           = "UNPAUSED"
  }

}
