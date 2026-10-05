from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, floor
)

spark = (
    SparkSession.builder
    .appName("CrashMapAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Read the cleaned accident data from HDFS
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("hdfs://localhost:9000/user/hive/warehouse/crashmap.db/accidents/indian_roads_dataset.csv")    

)

# Remove the CSV header row if it was interpreted as data
df = df.filter(col("accident_id").cast("int").isNotNull())

# 1. City-wise accident count
city_counts = (
    df.groupBy("city")
    .agg(count("*").alias("accident_count"))
    .orderBy(col("accident_count").desc())
)

print("\n=== ACCIDENTS BY CITY ===")
city_counts.show()

# 2. Hour-wise accident count
hour_counts = (
    df.groupBy("hour")
    .agg(count("*").alias("accident_count"))
    .orderBy("hour")
)

print("\n=== ACCIDENTS BY HOUR ===")
hour_counts.show(24)

# 3. Severity distribution
severity_counts = (
    df.groupBy("accident_severity")
    .agg(count("*").alias("accident_count"))
    .orderBy(col("accident_count").desc())
)

print("\n=== ACCIDENT SEVERITY ===")
severity_counts.show()

# 4. Spatial hotspot detection using 0.1-degree grid
hotspots = (
    df
    .withColumn("grid_lat", floor(col("latitude") * 10) / 10)
    .withColumn("grid_lon", floor(col("longitude") * 10) / 10)
    .groupBy("grid_lat", "grid_lon")
    .agg(count("*").alias("accident_count"))
    .orderBy(col("accident_count").desc())
)

print("\n=== TOP 10 SPATIAL HOTSPOTS ===")
hotspots.show(10)

# Save useful results as CSV
city_counts.coalesce(1).write.mode("overwrite").option("header", True).csv(
    "file:///home/anushree/CrashMap/output/city_counts"
)

hour_counts.coalesce(1).write.mode("overwrite").option("header", True).csv(
    "file:///home/anushree/CrashMap/output/hour_counts"
)

severity_counts.coalesce(1).write.mode("overwrite").option("header", True).csv(
    "file:///home/anushree/CrashMap/output/severity_counts"
)

hotspots.limit(20).coalesce(1).write.mode("overwrite").option("header", True).csv(
    "file:///home/anushree/CrashMap/output/hotspots"
)

spark.stop()
