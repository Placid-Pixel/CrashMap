CREATE DATABASE IF NOT EXISTS crashmap;

USE crashmap;

CREATE TABLE IF NOT EXISTS accidents (
    accident_id INT,
    city STRING,
    state STRING,
    latitude DOUBLE,
    longitude DOUBLE,
    accident_date DATE,
    accident_time STRING,
    accident_hour INT,
    day_of_week STRING,
    is_weekend BOOLEAN,
    road_type STRING,
    lanes INT,
    traffic_signal STRING,
    weather STRING,
    visibility DOUBLE,
    temperature DOUBLE,
    traffic_density STRING,
    cause STRING,
    accident_severity STRING,
    vehicles_involved INT,
    casualties INT,
    is_peak_hour BOOLEAN,
    festival STRING,
    risk_score DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

ALTER TABLE accidents
SET TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE IF NOT EXISTS accidents_clean
LIKE accidents;
