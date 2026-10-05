# Apache Flume Configuration

This directory contains the Apache Flume configuration used in the CrashMap project.

## Purpose

Apache Flume is used as the data ingestion layer to simulate streaming accident records and transfer them into HDFS.

## Data Flow

```text
Accident Stream CSV
        ↓
Flume Exec Source
        ↓
Memory Channel
        ↓
HDFS Sink
        ↓
HDFS: /crashmap/flume
```

## Configuration

The `crashmap-flume.conf` file contains the following components:

- **Source:** Exec source using `tail -F` to monitor the accident stream file.
- **Channel:** Memory channel for temporary event buffering.
- **Sink:** HDFS sink for storing incoming records in HDFS.
- **HDFS Path:** `/crashmap/flume`

## Streaming Simulation

For this academic project, streaming is simulated by continuously appending accident records to:

```text
data/stream/accident_stream.csv
```

Flume monitors this file and transfers newly received records to HDFS.

## Role in CrashMap

Flume provides the ingestion layer before HDFS storage and subsequent analysis using Hive and PySpark.

The overall pipeline is:

```text
Accident Dataset
      ↓
Flume
      ↓
HDFS
      ↓
Hive / PySpark
      ↓
Spatio-Temporal Analysis
      ↓
Streamlit Dashboard
```

## Technologies

- Apache Flume
- Hadoop HDFS
- Apache Hive
- Apache PySpark
- Python
- Streamlit

## Flume Configuration

The main configuration file is:

`crashmap-flume.conf`

It uses:

- **Exec Source** to monitor the accident stream file.
- **Memory Channel** to temporarily buffer incoming events.
- **HDFS Sink** to write the streamed records into HDFS.

## HDFS Output

The streamed data is stored under:

```text
/crashmap/flume
```

Flume automatically creates output files according to the configured rolling policy.

## Note

The streaming component is implemented as a simulation for the academic project. New accident records are appended to the stream file to demonstrate continuous data ingestion using Apache Flume.
