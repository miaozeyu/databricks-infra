-- Databricks notebook source
-- DBTITLE 1,NYC Taxi Data Copy
-- MAGIC %md
-- MAGIC ## Copy Data from samples.nyctaxi.trips to Our Table
-- MAGIC This notebook is part of a Terraform deployment that copies NYC taxi trip data to our own table using SQL.

-- COMMAND ----------

-- DBTITLE 1,Set Parameters
-- Define source and target tables
SELECT 
  'samples.nyctaxi.trips' AS source_table,
  'first_catalog.first_schema.trips' AS target_table;

-- COMMAND ----------

-- DBTITLE 1,Verify Source Table
-- Check if source table exists and show sample data
SELECT * 
FROM samples.nyctaxi.trips 
LIMIT 5;

-- COMMAND ----------

-- DBTITLE 1,Copy Data to Target Table
-- Create or replace the target table with data from source
CREATE OR REPLACE TABLE first_catalog.first_schema.trips AS
SELECT 
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  trip_distance,
  fare_amount,
  pickup_zip,
  dropoff_zip
FROM samples.nyctaxi.trips;

-- COMMAND ----------

-- DBTITLE 1,Verify Target Data
-- Show sample data from target table to verify
SELECT * 
FROM first_catalog.first_schema.trips 
LIMIT 5;
