````markdown
# CrashMap

## Road Accident Analysis and Hotspot Detection using Hadoop, Hive and PySpark

CrashMap is a Big Data analytics project developed to analyze road accident records and identify spatial and temporal accident patterns.

The project uses the Hadoop ecosystem for distributed storage and processing, Apache Flume for simulated streaming data ingestion, Apache Hive for SQL-based data warehousing and querying, Apache PySpark for large-scale data analysis, and Streamlit for interactive visualization.

> **Note:** The patterns and hotspot results presented by this project are based on the supplied accident dataset. They should not be interpreted as official real-world accident statistics.

## 1. Problem Statement

Road accident datasets can contain thousands or millions of records involving location, time, weather, road conditions, accident severity, and other factors.

Analyzing such large datasets using traditional methods can become difficult and time-consuming.

CrashMap addresses this problem by building a Big Data pipeline that:

- Stores accident data using HDFS.
- Simulates streaming data ingestion using Apache Flume.
- Uses Apache Hive for structured SQL-based analysis.
- Uses Apache PySpark for distributed data processing.
- Performs spatial and temporal accident analysis.
- Identifies accident hotspots using geographic grid-based analysis.
- Provides an interactive Streamlit dashboard for visualization.

## 2. Objectives

The main objectives of CrashMap are:

1. To store and manage accident data using Hadoop HDFS.
2. To demonstrate streaming data ingestion using Apache Flume.
3. To perform SQL-based analysis using Apache Hive.
4. To perform distributed data processing using PySpark.
5. To analyze accident patterns across cities and time periods.
6. To identify spatial accident hotspots using latitude and longitude.
7. To analyze accident severity, weather, causes, and days of the week.
8. To provide an interactive frontend using Streamlit.
9. To demonstrate a complete Big Data analytics pipeline.

## 3. System Architecture

```text
                   Accident Dataset
                         |
                         v
                 Data Preprocessing
                         |
                         v
                   Apache Flume
                 Streaming Ingestion
                         |
                         v
                     Hadoop HDFS
                         |
               +---------+---------+
               |                   |
               v                   v
          Apache Hive        Apache PySpark
          SQL Analysis     Distributed Analysis
               |                   |
               +---------+---------+
                         |
                         v
                Spatio-Temporal Analysis
                         |
                         v
                   Streamlit Dashboard
                         |
                         v
                Interactive Visualization
```

## 4. Big Data Technology Stack

| Technology     | Purpose                                        |
| -------------- | ---------------------------------------------- |
| Python         | Data preprocessing and application development |
| Apache Hadoop  | Big Data ecosystem                             |
| HDFS           | Distributed data storage                       |
| Apache Flume   | Streaming data ingestion                       |
| Apache Hive    | SQL-based data warehousing and querying        |
| Apache PySpark | Distributed data processing and analytics      |
| Streamlit      | Interactive dashboard and frontend             |
| Pandas         | Dataset preprocessing                          |
| Folium         | Interactive spatial map                        |
| Plotly         | Data visualization                             |
| Git/GitHub     | Version control and project hosting            |

## 5. Dataset

The project uses an accident dataset containing:

- **20,000 accident records**
- **24 attributes**

Important attributes include:

- Accident ID
- City
- State
- Latitude
- Longitude
- Date
- Time
- Hour
- Day of Week
- Weekend Indicator
- Road Type
- Number of Lanes
- Traffic Signal
- Weather
- Visibility
- Temperature
- Traffic Density
- Accident Cause
- Accident Severity
- Vehicles Involved
- Casualties
- Peak Hour Indicator
- Festival
- Risk Score

The dataset contains accident records from multiple Indian cities including:

- Delhi
- Mumbai
- Chandigarh
- Bangalore
- Kolkata
- Hyderabad
- Chennai
- Pune

## 6. Data Preprocessing

The raw accident dataset is cleaned before analysis.

The preprocessing stage includes:

- Checking for duplicate records.
- Handling missing values.
- Validating accident IDs.
- Preparing date and time attributes.
- Preparing geographic coordinates.
- Preparing categorical attributes.
- Generating the processed dataset used by the analytics pipeline.

The project dataset contained 20,000 original records and no duplicate records.

## 7. Apache Flume

Apache Flume is used as the data ingestion layer.

For this academic project, streaming is simulated by continuously appending accident records to a stream file.

### Flume Pipeline

```text
Accident Stream CSV
        |
        v
    Exec Source
        |
        v
   Memory Channel
        |
        v
     HDFS Sink
        |
        v
 HDFS: /crashmap/flume
```

The Flume configuration is available in:

```text
flume/crashmap-flume.conf
```

The Flume documentation is available in:

```text
flume/README.md
```

## 8. Hadoop HDFS

Hadoop Distributed File System (HDFS) is used to store the accident data in a distributed file system.

The project uses HDFS as the storage layer between data ingestion and data analysis.

Example HDFS locations used by the project include:

```text
/crashmap
/crashmap/flume
/user/hive/warehouse/crashmap.db
```

HDFS provides scalable storage for large datasets.

## 9. Apache Hive

Apache Hive is used as the data warehousing and SQL analysis layer.

The project creates a Hive database named:

```text
crashmap
```

Main tables include:

```text
accidents
accidents_clean
```

Hive is used for:

- Total accident count
- City-wise accident analysis
- Hour-wise accident analysis
- Severity analysis
- Weather analysis
- Cause analysis
- Day-of-week analysis
- Spatial hotspot analysis

The Hive scripts are available in:

```text
hive/create_tables.sql
hive/analysis_queries.sql
hive/README.md
```

## 10. Apache PySpark

Apache PySpark is used as the distributed data processing engine.

PySpark performs:

- City-wise aggregation
- Hour-wise aggregation
- Accident severity analysis
- Spatial hotspot detection
- Generation of analytical output files

The main PySpark program is:

```text
scripts/pyspark_analysis.py
```

Spatial analysis is performed by dividing the geographic coordinates into a grid.

A grid size of approximately 0.1 degrees is used to group accident locations.

```text
Latitude  → Spatial Grid
Longitude → Spatial Grid
                |
                v
         Accident Count
                |
                v
       Top Spatial Hotspots
```

## 11. Spatio-Temporal Analysis

CrashMap performs both spatial and temporal analysis.

### Spatial Analysis

Spatial analysis answers:

> **WHERE are accidents concentrated?**

Latitude and longitude are converted into geographic grid cells.

The number of accidents in each grid cell is calculated.

### Temporal Analysis

Temporal analysis answers:

> **WHEN do accidents occur more frequently?**

The project analyzes:

- Hour of the day
- Day of the week
- Peak hours
- Weekdays vs weekends

Combining spatial and temporal analysis helps identify accident patterns based on both location and time.

## 12. Streamlit Dashboard

CrashMap provides an interactive frontend using Streamlit.

The dashboard allows users to filter accident records by:

- City
- Day of Week
- Weather
- Accident Severity

The dashboard displays:

- Total accident count
- Peak accident hour
- Top city
- Most common accident severity
- Spatial hotspot
- City-wise accident chart
- Hour-wise accident chart
- Severity chart
- Day-wise accident chart
- Spatial hotspot table
- Interactive geographic map

The dashboard application is available at:

```text
dashboard/app.py
```

## 13. Sample Analysis Results

The following results were obtained from the supplied dataset.

### Accidents by City

| City       | Accident Count |
| ---------- | -------------- |
| Chandigarh | 2577           |
| Chennai    | 2575           |
| Kolkata    | 2559           |
| Pune       | 2517           |
| Mumbai     | 2492           |
| Bangalore  | 2438           |
| Delhi      | 2433           |
| Hyderabad  | 2409           |

### Peak Observed Hour

The highest accident count in the dataset occurs at:

```text
02:00
```

with:

```text
888 accidents
```

### Accident Severity

| Severity | Count  | Percentage |
| -------- | ------ | ---------- |
| Minor    | 11,025 | 55.1%      |
| Major    | 5,988  | 29.9%      |
| Fatal    | 2,987  | 14.9%      |

### Weather Distribution

| Weather | Count |
| ------- | ----- |
| Clear   | 6,690 |
| Rain    | 6,677 |
| Fog     | 6,633 |

### Main Accident Causes

| Cause         | Count |
| ------------- | ----- |
| Distraction   | 4,026 |
| Overspeeding  | 4,025 |
| Weather       | 3,997 |
| Drunk Driving | 3,978 |
| Poor Road     | 3,974 |

## 14. Spatial Hotspot Detection

The project divides the geographic region into approximately 0.1-degree grid cells.

The highest accident concentrations observed in the supplied dataset include:

| Grid Latitude | Grid Longitude | Accident Count |
| ------------- | -------------- | -------------- |
| 30.7          | 76.8           | 688            |
| 30.6          | 76.7           | 679            |
| 30.6          | 76.8           | 632            |
| 30.7          | 76.7           | 578            |
| 13.1          | 80.1           | 377            |
| 12.8          | 80.1           | 345            |
| 12.9          | 80.2           | 342            |
| 22.5          | 88.4           | 329            |

These values represent spatial patterns within the supplied dataset.

They do not represent official government accident statistics.

## 15. Project Structure

```text
CrashMap/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dashboard/
│   └── app.py
│
├── flume/
│   ├── crashmap-flume.conf
│   └── README.md
│
├── hive/
│   ├── create_tables.sql
│   ├── analysis_queries.sql
│   └── README.md
│
├── scripts/
│   └── pyspark_analysis.py
│
├── output/
│
├── screenshots/
│
├── requirements.txt
├── .gitignore
└── README.md
```

Large datasets and generated output files are excluded from GitHub using `.gitignore`.

## 16. Installation Requirements

The project was developed and tested on Ubuntu Linux.

Required software:

- Java 17
- Hadoop 3.x
- Apache Hive 4.x
- Apache Flume 1.x
- Apache PySpark
- Python 3
- Streamlit
- Git

Python dependencies are listed in:

```text
requirements.txt
```

## 17. Running the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/Placid-Pixel/CrashMap.git
cd CrashMap
```

### Step 2: Create Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start Hadoop HDFS

```bash
start-dfs.sh
```

Verify Hadoop processes:

```bash
jps
```

The NameNode and DataNode should be running.

### Step 5: Start HiveServer2

```bash
hive \
--hiveconf hive.server2.thrift.port=10001 \
--hiveconf hive.server2.thrift.bind.host=127.0.0.1 \
--hiveconf hive.server2.transport.mode=binary \
--service hiveserver2
```

### Step 6: Run PySpark Analysis

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
python scripts/pyspark_analysis.py
```

### Step 7: Run Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard can then be opened in a browser.

## 18. Running Flume

The Flume configuration is available at:

```text
flume/crashmap-flume.conf
```

Flume can be started using:

```bash
flume-ng agent \
--conf conf \
--conf-file flume/crashmap-flume.conf \
--name crashmap \
-Dflume.root.logger=INFO,console
```

The streaming simulation works by appending records to:

```text
data/stream/accident_stream.csv
```

Flume monitors the file and transfers new records into HDFS.

## 19. Project Workflow

The complete CrashMap workflow is:

```text
1. Accident Dataset
        ↓
2. Data Preprocessing
        ↓
3. Flume Streaming Simulation
        ↓
4. HDFS Storage
        ↓
5. Hive Data Warehousing
        ↓
6. PySpark Distributed Processing
        ↓
7. Spatial + Temporal Analysis
        ↓
8. Result Generation
        ↓
9. Streamlit Dashboard
```

## 20. Key Features

- Big Data storage using Hadoop HDFS
- Streaming ingestion using Apache Flume
- SQL-based analysis using Apache Hive
- Distributed processing using Apache PySpark
- Spatial hotspot detection
- Temporal accident analysis
- Accident severity analysis
- Weather and cause analysis
- Interactive filtering
- Interactive geographic visualization
- Streamlit-based frontend
- GitHub-based project management

## 21. Limitations

The project has the following limitations:

- Streaming is simulated rather than connected to a live accident sensor system.
- The dataset is used for academic analysis.
- Hotspots are identified using geographic grid aggregation.
- The results represent patterns in the supplied dataset and are not official accident statistics.
- No machine learning model is used for accident prediction.

## 22. Future Scope

The project can be extended by:

- Integrating real-time accident data sources.
- Adding Kafka for real-time event streaming.
- Adding real-time dashboards.
- Using larger datasets distributed across multiple nodes.
- Adding predictive analytics.
- Integrating external geographic data.
- Adding advanced spatial analysis.
- Deploying the system on a cloud-based Hadoop cluster.

## 23. Conclusion

CrashMap demonstrates a complete Big Data analytics pipeline for road accident analysis.

The project integrates:

```text
Apache Flume
      +
Hadoop HDFS
      +
Apache Hive
      +
Apache PySpark
      +
Streamlit
```

The system demonstrates how large accident datasets can be ingested, stored, queried, processed, and visualized using Big Data technologies.

The project focuses on identifying spatial and temporal accident patterns and presenting the results through an interactive dashboard.

## 24. Academic Relevance

CrashMap demonstrates the following Big Data concepts:

- Distributed storage
- HDFS
- Data ingestion
- Stream processing concepts
- Data warehousing
- SQL-based Big Data analysis
- Distributed data processing
- Spatial data analytics
- Temporal data analytics
- Interactive data visualization

## 25. Author

**CrashMap**

Road Accident Analysis and Hotspot Detection using Hadoop, Hive and PySpark.

GitHub Repository:

https://github.com/Placid-Pixel/CrashMap
````
