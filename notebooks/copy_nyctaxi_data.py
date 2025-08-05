# Databricks notebook source
# DBTITLE 1,NYC Taxi Data Copy
# MAGIC %md
# MAGIC ## Copy Data from samples.nyctaxi.trips to Our Table
# MAGIC This notebook is part of a Terraform deployment that copies NYC taxi trip data to our own table using SQL.

# COMMAND ----------

# DBTITLE 1,Set Parameters
-- Create widgets for parameters
CREATE WIDGET TEXT source_catalog DEFAULT 'samples';
CREATE WIDGET TEXT source_schema DEFAULT 'nyctaxi';
CREATE WIDGET TEXT source_table DEFAULT 'trips';
CREATE WIDGET TEXT target_catalog DEFAULT 'first_catalog';
CREATE WIDGET TEXT target_schema DEFAULT 'first_schema';
CREATE WIDGET TEXT target_table DEFAULT 'trips';

-- Get parameter values
SET source_path = CONCAT('${source_catalog}.${source_schema}.${source_table}');
SET target_path = CONCAT('${target_catalog}.${target_schema}.${target_table}');

-- Display parameters
SELECT 
  '${source_path}' AS source_table,
  '${target_path}' AS target_table;

# COMMAND ----------

-- DBTITLE 1,Verify Source Table
-- Check if source table exists and show sample data
SELECT * FROM ${source_path} LIMIT 5;

# COMMAND ----------

-- DBTITLE 1,Copy Data to Target Table
-- Create or replace the target table with data from source
CREATE OR REPLACE TABLE ${target_path} AS
SELECT 
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  trip_distance,
  fare_amount,
  pickup_zip,
  dropoff_zip
FROM ${source_path};

-- Get row count for verification
SELECT 
  '${target_path}' AS table_name,
  COUNT(*) AS row_count 
FROM ${target_path};

# COMMAND ----------

-- DBTITLE 1,Verify Target Data
-- Show sample data from target table to verify
SELECT * FROM ${target_path} LIMIT 5;

# COMMAND ----------

-- DBTITLE 1,Clean Up Widgets
-- Remove all widgets
REMOVE WIDGET source_catalog;
REMOVE WIDGET source_schema;
REMOVE WIDGET source_table;
REMOVE WIDGET target_catalog;
REMOVE WIDGET target_schema;
REMOVE WIDGET target_table;
