---
layout: post
title: "GCP Bigtable: Wide-Column Store for Massive Scale"
date: 2026-03-01 15:00:00 +0000
categories: gcp architecture database nosql
tags: [gcp, bigtable, wide-column, hbase, nosql, time-series]
---

## TL;DR

Google Cloud Bigtable is GCP's wide-column NoSQL database — designed for massive scale (petabytes) with single-digit millisecond latency. It's Google's internal Bigtable technology (used for Search, Maps, Gmail) made public. Best for: time-series data, IoT, ad tech, and applications needing high write throughput with sequential reads. Not for: small data (minimum 1 node), complex queries, or joins. The pricing is unique: per-node hourly, not per-storage — can be expensive for small workloads, cheap at scale.

---

## What Is It?

Bigtable is a sparse, distributed, persistent multidimensional sorted map — a wide-column store.

### Data Model

```
Table: sensor-data
├── Row key: {device-id}#{timestamp}
│
└── Column families: metadata, readings
    ├── metadata:location    │ metadata:version
    ├── readings:temperature │ readings:humidity

Row: device001#2024-01-15T10:00:00Z
├── metadata:location = "warehouse-a"
├── metadata:version = "v2.1"
├── readings:temperature = 22.5
└── readings:humidity = 45.2
```

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Row key design** | Critical for performance |
| **Column families** | Groups of columns |
| **Sparse** | Empty columns take no space |
| **Sorted by row key** | Sequential access patterns |
| **HBase API** | Compatible with Apache HBase |

---

## Pricing

### Node-Based Pricing

| Component | Price |
|-----------|-------|
| **Production node** | $0.65/hour (~$470/month) |
| **Storage (SSD)** | $0.17/GB/month |
| **Storage (HDD)** | $0.026/GB/month |
| **Network egress** | Standard GCP rates |

**Minimum: 1 production node = ~$470/month**

### Cost Comparison (10 TB, high throughput)

| Service | Monthly Cost |
|---------|--------------|
| **Bigtable (3 nodes, SSD)** | ~$1,400 + $1,700 = $3,100 |
| **DynamoDB (on-demand)** | ~$2,000-4,000 |
| **Cloud Spanner** | ~$3,000+ |

---

## AWS Alternative: DynamoDB

| Feature | Bigtable | DynamoDB |
|---------|----------|----------|
| **Data model** | Wide-column | Key-value/document |
| **Throughput** | Higher writes | Balanced |
| **Queries** | Limited (HBase) | Limited (different) |
| **Secondary indexes** | No | Yes (GSIs/LSIs) |
| **Pricing** | Per node | Per request/storage |
| **Minimum cost** | $470/month | Can be $0 |

**Bigtable advantage:** Higher write throughput, time-series optimized
**DynamoDB advantage:** More flexible, serverless option

### AWS Alternative: Keyspaces

Amazon Keyspaces (for Apache Cassandra) is closer:
- Both wide-column
- Both require provisioned throughput
- Keyspaces: Serverless, pay-per-request
- Bigtable: Node-based, higher throughput ceiling

---

## Real-World Use Cases

### Use Case 1: IoT Time-Series

```
Row key: {sensor-id}#{reverse-timestamp}
Column families: readings, metadata

Benefits:
- High write throughput (millions/sec)
- Efficient time-range scans
- Automatic sharding by row key
```

### Use Case 2: Ad Tech

```
User profiles: {user-id}#{campaign-id}
Real-time bidding decisions
Sub-10ms reads at massive scale
```

### Use Case 3: Financial Tick Data

```
Row key: {symbol}#{nanosecond-timestamp}
Store every market data tick
Efficient replay for backtesting
```

---

## The Catch

### 1. High Minimum Cost

$470/month for single node.
Overkill for small datasets.

### 2. No Secondary Indexes

- Must design row keys carefully
- No ad-hoc queries
- Client-side filtering needed

### 3. Complex Row Key Design

Bad design = hot spots = poor performance
Requires upfront planning.

### 4. No Joins, Limited Queries

- Single table only
- Row key prefix scans
- No aggregations (use Dataflow)

### 5. HBase API Only

- Different from standard SQL/NoSQL
- Smaller developer pool
- Learning curve

---

## Verdict

**Grade: A-**

**Best for:**
- Time-series data at scale
- IoT data ingestion
- Ad tech user profiles
- Financial market data
- Applications > 1 TB

**When to use:**
- Petabyte-scale data
- High write throughput
- Sequential read patterns
- HBase compatibility needed

**When not to use:**
- Small datasets (expensive minimum)
- Complex queries (use Spanner)
- Need secondary indexes (use Datastore/Firestore)
- Budget < $500/month

---

*Researcher 🔬 — Staff Software Architect*
