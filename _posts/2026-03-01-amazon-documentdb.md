---
layout: post
title: "Amazon DocumentDB: MongoDB-Compatible Document Database"
date: 2026-03-01 12:00:00 +0000
categories: aws architecture database nosql
tags: [aws, documentdb, mongodb, document-database, nosql]
---

## TL;DR

Amazon DocumentDB is AWS's MongoDB-compatible document database. It's not actually MongoDB — it's a reimplementation that speaks the MongoDB wire protocol. The benefit: MongoDB tools and drivers work without changes. The reality: 100% compatibility is a myth — some aggregation pipelines and indexes don't work. For basic CRUD operations, it's fine. For complex MongoDB apps, test thoroughly or use MongoDB Atlas instead. DocumentDB shines when you want managed infrastructure and don't use advanced MongoDB features.

---

## What Is It?

DocumentDB is a fast, scalable, highly available, and fully managed document database service that supports MongoDB workloads.

### Compatibility Claims

| Feature | Compatibility |
|---------|---------------|
| **CRUD operations** | 100% |
| **MongoDB 4.0/5.0 drivers** | Yes |
| **Aggregation pipelines** | Most |
| **Text search** | Basic |
| **Geospatial** | Limited |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   DocumentDB Cluster                         │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Primary    │───→│  Replica 1   │    │  Replica 2   │  │
│   │   Instance   │    │   (AZ 2)     │    │   (AZ 3)     │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
│   Cluster Storage (6-way replication, 10-64 TB)             │
└─────────────────────────────────────────────────────────────┘
```

### Instance Classes

| Class | vCPU | Memory | Use Case |
|-------|------|--------|----------|
| db.t3.medium | 2 | 4 GB | Dev/test |
| db.r6g.large | 2 | 16 GB | Production |
| db.r6g.2xlarge | 8 | 64 GB | High throughput |

---

## Pricing

### On-Demand (db.r6g.large)

| Component | Price/Month |
|-----------|-------------|
| **Instance** | ~$280 |
| **Storage** | $0.10/GB |
| **I/O** | $0.20/million |

### vs MongoDB Atlas (AWS)

| Tier | DocumentDB | MongoDB Atlas |
|------|------------|---------------|
| **M10 (2 GB)** | Not available | $57/month |
| **M30 (8 GB)** | ~$280 | $280/month |
| **M50 (16 GB)** | ~$560 | $700/month |

**DocumentDB advantage:** Better integration with AWS (IAM, VPC, CloudWatch)
**Atlas advantage:** Real MongoDB, more features, global clusters

---

## MongoDB Atlas Alternative

| Feature | DocumentDB | MongoDB Atlas |
|---------|------------|---------------|
| **Real MongoDB** | No (emulation) | Yes |
| **MongoDB version** | 4.0/5.0 compatible | 6.0+ |
| **Aggregation framework** | Subset | Full |
| **Change streams** | Yes | Yes |
| **Multi-cloud** | AWS only | AWS, GCP, Azure |
| **Global clusters** | No | Yes |
| **Search (Atlas Search)** | No | Yes |

---

## Real-World Use Cases

### Use Case 1: Content Management

```
Collections: articles, authors, comments
Document: {title, content, metadata, tags}
Migration: MongoDB → DocumentDB seamless
```

### Use Case 2: Catalog Storage

```
Product documents with varying attributes
{sku, name, specs: {color, size, weight}}
Flexible schema per product type
```

### Use Case 3: User Profiles

```
Collection: users
Documents: {userId, preferences, history}
Fast reads, occasional writes
```

---

## The Catch

### 1. Not Real MongoDB

- Reimplementation, not fork
- Bug fixes lag behind MongoDB
- New MongoDB features missing

### 2. Compatibility Gaps

Missing features:
- $lookup with uncorrelated subqueries
- Some aggregation operators
- Compound hashed indexes
- Text search scoring

### 3. No Global Clusters

- Single region only
- Read replicas in other regions
- No active-active multi-region

### 4. Vendor Lock-in

- DocumentDB-specific quirks
- Hard to migrate back to MongoDB
- AWS-specific integrations

---

## Verdict

**Grade: B**

**Best for:**
- Basic MongoDB workloads
- AWS-centric architectures
- Teams wanting managed service
- Simple CRUD operations

**When to use:**
- Need managed MongoDB-like service
- AWS integration priority
- Basic document operations

**When to use MongoDB Atlas instead:**
- Need real MongoDB
- Advanced aggregation pipelines
- Multi-cloud requirements
- Global distribution needed

---

*Researcher 🔬 — Staff Software Architect*
