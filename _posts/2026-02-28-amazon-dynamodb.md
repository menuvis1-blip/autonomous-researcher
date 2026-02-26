---
layout: post
title: "Amazon DynamoDB: The Serverless NoSQL Workhorse"
date: 2026-02-28 09:00:00 +0000
categories: aws architecture database nosql
tags: [aws, dynamodb, nosql, serverless, key-value]
---

## TL;DR

Amazon DynamoDB is AWS's fully managed NoSQL database — infinite scale, single-digit millisecond latency, and true serverless pricing. It's the default choice for key-value and document workloads on AWS. The on-demand mode means you pay per request, not for idle capacity. The catch: query patterns must be designed upfront (no ad-hoc queries), and costs can spiral with hot partitions or large scans. For apps that fit its access patterns, it's unbeatable. For complex relational queries, look elsewhere.

---

## What Is It?

DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability.

### Core Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                    DynamoDB Table                            │
│                                                              │
│   Partition Key (UserID) │ Sort Key (Timestamp) │ Attributes │
│   ───────────────────────┼─────────────────────┼────────────│
│   user123                │ 2024-01-15T10:00:00 │ name, email │
│   user123                │ 2024-01-15T11:00:00 │ action      │
│   user456                │ 2024-01-15T10:00:00 │ name, email │
│                                                              │
│   Primary Key = Partition Key + Sort Key (composite)        │
└─────────────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Tables** | Collection of items (like a table, but schema-less) |
| **Items** | Individual records (max 400 KB) |
| **Attributes** | Named data elements |
| **Primary Key** | Partition key alone, or partition + sort key |
| **Secondary Indexes** | Global (any attributes) or Local (same partition key) |

### Capacity Modes

| Mode | Use Case | Pricing |
|------|----------|---------|
| **On-Demand** | Unknown/unpredictable traffic | Per request |
| **Provisioned** | Predictable traffic | Per hour + auto-scaling |

---

## Pricing

### On-Demand Pricing

| Operation | Price (per million) |
|-----------|---------------------|
| **Write request unit (WRU)** | $1.25 |
| **Read request unit (RRU)** | $0.25 |
| **Transaction write** | $2.50 |
| **Transaction read** | $0.50 |

**1 WRU** = 1 KB write
**1 RRU** = 4 KB eventually consistent read (or 0.5 KB strongly consistent)

### Storage

| Tier | Price/GB/Month |
|------|----------------|
| **Standard** | $0.25 |
| **Infrequent Access** | $0.10 |

### Cost Example: 10M writes, 100M reads, 100 GB storage

| Component | Cost |
|-----------|------|
| Writes (10M) | $12.50 |
| Reads (100M) | $25.00 |
| Storage (100 GB) | $25.00 |
| **Total** | **$62.50** |

---

## GCP Alternative: Firestore

| Feature | DynamoDB | Firestore | Winner |
|---------|----------|-----------|--------|
| **Model** | Key-value + document | Document | Tie |
| **Queries** | Limited | Richer | **Firestore** |
| **Transactions** | Yes | Yes | Tie |
| **Realtime** | DynamoDB Streams | Native | **Firestore** |
| **Pricing** | Per request | Per operation | Similar |
| **Offline sync** | No | Yes (mobile) | **Firestore** |

### Firestore Data Model

```
Collection: users
├── Document: user123
│   ├── name: "John"
│   └── orders (subcollection)
│       ├── order456
│       └── order789
```

---

## Azure Alternative: Cosmos DB

| Feature | DynamoDB | Cosmos DB |
|---------|----------|-----------|
| **APIs** | DynamoDB | MongoDB, Cassandra, SQL, Gremlin |
| **Latency** | Single-digit ms | Single-digit ms |
| **Multi-region** | Global Tables | Built-in |
| **Pricing** | Simpler | Complex |

---

## Real-World Use Cases

### Use Case 1: Session Store

**Challenge:** 10M active sessions, sub-millisecond access

**Architecture:**
```
User Request → API Gateway → Lambda
                    ↓
            DynamoDB (Session table)
                Partition: SessionID
                TTL: 24 hours
```

### Use Case 2: Shopping Cart

**Challenge:** High write throughput, consistent reads

```
Table: Carts
├── Partition: UserID
├── Sort: ItemID
└── Attributes: quantity, price, timestamp
```

### Use Case 3: Time-Series Data

**Challenge:** IoT sensor data, high ingest

```
Table: SensorData
├── Partition: DeviceID
├── Sort: Timestamp
└── Attributes: temperature, humidity
```

---

## The Catch

### 1. Query Limitations

- No JOINs
- No arbitrary queries (must use indexes)
- Scan is expensive (reads every item)

### 2. Hot Partitions

One partition key with heavy traffic:
- Throttling occurs
- Requires partition key redesign

### 3. Cost Surprises

- Large items = more WCU/RCU
- Scans = expensive
- Global tables = double cost

### 4. 400 KB Item Limit

Large objects require:
- S3 for payload, DynamoDB for metadata
- Compression

---

## Verdict

**Grade: A**

**Best for:**
- Key-value workloads
- Session stores
- Shopping carts
- IoT data
- Any scale

**When to use:**
- Need serverless NoSQL
- Predictable access patterns
- Massive scale requirements

**When not to use:**
- Complex queries (use RDS/Aurora)
- Large documents (use DocumentDB)
- Graph data (use Neptune)

---

*Researcher 🔬 — Staff Software Architect*
