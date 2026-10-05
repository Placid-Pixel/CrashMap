# Hive Scripts

This directory contains the Apache Hive SQL scripts used in the CrashMap project.

## Files

- `create_tables.sql` - Creates the CrashMap database and accident tables.
- `analysis_queries.sql` - Contains Hive queries for accident aggregation and spatial analysis.

## Main Hive Operations

Hive is used for:

- Data warehousing
- SQL-based accident analysis
- City-wise aggregation
- Time-wise aggregation
- Accident severity analysis
- Weather and cause analysis
- Spatial hotspot identification

The processed accident data is stored in HDFS and accessed through Hive.

## Big Data Role

Hive provides a SQL abstraction layer over data stored in HDFS, allowing large datasets to be queried using SQL-like commands.
