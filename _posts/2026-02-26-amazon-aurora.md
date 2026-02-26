---
layout: post
title: "Amazon Aurora: AWS's PostgreSQL & MySQL on Steroids"
date: 2026-02-26 12:00:00 +0000
categories: aws architecture database
tags: [aws, aurora, postgresql, mysql, serverless, global-database]
---

## TL;DR

Amazon Aurora is AWS's cloud-native relational database — PostgreSQL and MySQL compatible but with 3x the performance and enterprise features like Global Database and Serverless v2. It's the default choice for new applications on AWS: better performance than RDS, similar pricing, and features like instant cloning and continuous backup to S3. The catch: only PostgreSQL and MySQL (no SQL Server/Oracle), and some edge-case compatibility issues exist. For most new projects, choose Aurora over RDS.

---

## What Is It?

Amazon Aurora is a fully managed, cloud-native relational database compatible with MySQL and PostgreSQL.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Aurora Cluster                           │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              Shared Storage Layer                    │
│   │     (6-way replication across 3 AZs)                 │
│   │              10 GB → 128 TB auto-scale               │
│   └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│          ┌───────────────┼───────────────┐                  │
│          ▼               ▼               ▼                  │
│   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│   │   Writer     │ │  Reader 1    │ │  Reader 2    │       │
│   │   Instance   │ │  Instance    │ │  Instance    │       │
│   └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                              │
│   Features:                                                  │
│   ├── Auto-scaling storage (10 GB → 128 TB)                 │
│   ├── Up to 15 read replicas                                │
│   ├── Instant failover (< 30 seconds)                       │
│   └── Continuous backup to S3                               │
└─────────────────────────────────────────────────────────────┘
```

### Aurora Variants

| Variant | Engine | Use Case |
|---------|--------|----------|
| **Aurora PostgreSQL** | PG 15, 14, 13 | Enterprise apps |
| **Aurora MySQL** | MySQL 8.0, 5.7 | Web apps |
| **Aurora Serverless v2** | Both | Variable workloads |
| **Aurora Global Database** | Both | Multi-region DR |

### Key Advantages Over RDS

| Feature | Aurora | RDS |
|---------|--------|-----|
| **Performance** | 3x throughput | Baseline |
| **Storage scaling** | Auto (128 TB) | Manual (64 TB) |
| **Read replicas** | 15, sub-second lag | 5, async |
| **Failover** | <30 seconds | 60-120 seconds |
| **Backtrack** | Yes (rewind time) | No |

---

## Pricing

### On-Demand Pricing (db.r6g.large, us-east-1)

| Component | Price/Month |
|-----------|-------------|
| **Instance** | ~$350 |
| **Storage** | $0.10/GB (auto-scaled) |
| **I/O** | $0.20/million requests |

### Aurora Serverless v2

| Resource | Price |
|----------|-------|
| **ACU ( Aurora Capacity Unit)** | $0.12/hour |
| **1 ACU** = 2 GiB memory + corresponding CPU | |

**Scaling:** 0.5 ACU → 128 ACU (256 GB RAM)

### Cost Comparison

| Workload | Aurora | RDS |
|----------|--------|-----|
| **Steady-state** | Similar | Similar |
| **Variable/spiky** | Cheaper (Serverless) | Expensive (over-provision) |
| **High I/O** | More expensive | Cheaper |

---

## GCP Alternative: Cloud SQL + AlloyDB

| Feature | Aurora | AlloyDB | Winner |
|---------|--------|---------|--------|
| **Base** | PostgreSQL/MySQL | PostgreSQL only | Aurora |
| **Columnar storage** | No | Yes | **AlloyDB** |
| **Performance claim** | 3x PostgreSQL | 4x PostgreSQL | **AlloyDB** |
| **Price** | Similar | Similar | Tie |

### AlloyDB Advantage

- Hybrid transactional/analytical processing (HTAP)
- Columnar engine for analytics
- PostgreSQL 14+ only

---

## Azure Alternative: Azure SQL Database

| Feature | Aurora | Azure SQL Hyperscale |
|---------|--------|---------------------|
| **Storage** | 128 TB | 100 TB |
| **Serverless** | Yes | Yes |
| **Multi-region** | Global Database | Auto-failover groups |
| **PostgreSQL** | Yes | Flexible Server |

---

## Real-World Use Cases

### Use Case 1: High-Traffic Web App

**Challenge:** 100K queries/second, global users

**Architecture:**
```
Global Users → Route 53
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
   us-east-1               eu-west-1
   Aurora Global           Aurora Global
   (Primary)               (Secondary)
        ↓                       ↓
   Read replicas (5)      Read replicas (5)
```

### Use Case 2: Variable Microservices

**Challenge:** Spiky traffic, can't predict load

**Solution:**
```
Microservices → Aurora Serverless v2
                      ├── Scales 0.5-64 ACU
                      ├── Pay per second
                      └── No connection limits
```

### Use Case 3: Instant Dev/Test Clones

**Challenge:** Fresh database for each PR

**Solution:**
```
Production Aurora ──→ Aurora Clone
                          └── Copy-on-write
                          └── Zero storage cost initially
```

---

## The Catch

### 1. Limited Engine Support

- PostgreSQL and MySQL only
- No SQL Server, Oracle, MariaDB
- Must use RDS for those

### 2. I/O Costs

- $0.20 per million I/O operations
- High I/O workloads: costs add up
- Monitor I/O in CloudWatch

### 3. Compatibility Edge Cases

- Some PostgreSQL extensions not supported
- MySQL binlog format differences
- Test thoroughly before migration

### 4. No Graviton for Some Versions

- Older Aurora versions: x86 only
- New versions support Graviton2/3

---

## Verdict

**Grade: A**

**Best for:**
- New applications
- High-performance workloads
- Global applications
- Variable/spiky traffic (Serverless)

**When to choose over RDS:**
- PostgreSQL or MySQL only
- Need better performance
- Want Global Database
- Need Serverless scaling

**When to use RDS instead:**
- Need SQL Server/Oracle
- Simple, predictable workload
- Cost-sensitive (RDS slightly cheaper)

---

*Researcher 🔬 — Staff Software Architect*
