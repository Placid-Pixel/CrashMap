USE crashmap;

-- Total number of accident records
SELECT COUNT(*) AS total_accidents
FROM accidents_clean;


-- Accidents by city
SELECT
    city,
    COUNT(*) AS accident_count
FROM accidents_clean
GROUP BY city
ORDER BY accident_count DESC;


-- Accidents by hour
SELECT
    accident_hour,
    COUNT(*) AS accident_count
FROM accidents_clean
GROUP BY accident_hour
ORDER BY accident_hour;


-- Accidents by severity
SELECT
    accident_severity,
    COUNT(*) AS accident_count
FROM accidents_clean
GROUP BY accident_severity
ORDER BY accident_count DESC;


-- Accidents by weather
SELECT
    weather,
    COUNT(*) AS accident_count
FROM accidents_clean
GROUP BY weather
ORDER BY accident_count DESC;


-- Accidents by cause
SELECT
    cause,
    COUNT(*) AS accident_count
FROM accidents_clean
GROUP BY cause
ORDER BY accident_count DESC;


-- Accidents by day of week
SELECT
    day_of_week,
    COUNT(*) AS accident_count
FROM accidents_clean
GROUP BY day_of_week
ORDER BY accident_count DESC;


-- Spatial hotspot analysis using 0.1 degree grid
SELECT
    FLOOR(latitude * 10) / 10 AS grid_lat,
    FLOOR(longitude * 10) / 10 AS grid_lon,
    COUNT(*) AS accident_count
FROM accidents_clean
GROUP BY
    FLOOR(latitude * 10) / 10,
    FLOOR(longitude * 10) / 10
ORDER BY accident_count DESC
LIMIT 20;
