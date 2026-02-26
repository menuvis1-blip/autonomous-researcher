---
layout: post
title: "GCP Cloud SQL & AlloyDB: Google's Database Duo"
date: 2026-02-26 15:00:00 +0000
categories: gcp architecture database
tags: [gcp, cloud-sql, alloydb, postgresql, mysql, htap]
---

## TL;DR

GCP Cloud SQL is Google's managed MySQL and PostgreSQL — simpler than AWS RDS but fewer enterprise features. AlloyDB is GCP's answer to Aurora: PostgreSQL-compatible with 4x performance and columnar storage for analytics. Cloud SQL is the safe, boring choice for standard apps. AlloyDB is the power play when you need HTAP (hybrid transactional/analytical) in one database. The catch: AlloyDB is PostgreSQL-only, and both are more expensive than self-managed.

---

## What Is It?

### Cloud SQL

Fully managed MySQL and PostgreSQL for standard applications.

```
┌─────────────────────────────────────────────────────────────┐
│                     Cloud SQL Instance                       │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Primary    │───→│   Replica    │    │   Backups    │  │
│   │   Instance   │    │   (region)   │    │   (7 days)   │  │
│   └──────┬───────┘    └──────────────┘    └──────────────┘  │
│          │                                                   │
│   ┌──────┴───────┐                                           │
│   │ Auto-scaling │  Storage grows automatically              │
│   │ Maintenance  │  Managed patches                          │
│   │ IAM auth     │  Google Cloud auth                        │
│   └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

**Engines:**
- PostgreSQL 16, 15, 14, 13, 12, 11, 10, 9.6
- MySQL 8.0, 5.7, 5.6

### AlloyDB

High-performance PostgreSQL with analytics capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│                      AlloyDB Cluster                         │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              Columnar Storage Engine                 │   │
│   │         (For analytical queries)                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              Row-Based Storage (OLTP)                │   │
│   │         (For transactional queries)                  │   │
│   └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│          ┌───────────────┼───────────────┐                  │
│          ▼               ▼               ▼                  │
│   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│   │   Primary    │ │  Replica 1   │ │  Replica 2   │       │
│   │   (Read/Write)│ │  (Read)      │ │  (Read)      │       │
│   └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

**Key features:**
- 4x PostgreSQL performance
- Columnar engine for analytics
- AI/ML integration (Vertex AI)
- Cross-region replication

---

## Pricing

### Cloud SQL Pricing (db-n1-standard-2)

| Component | Price/Month |
|-----------|-------------|
| **Instance** | ~$100 |
| **Storage** | $0.17/GB (SSD) |
| **Backup storage** | $0.08/GB |

### AlloyDB Pricing

| Component | Price |
|-----------|-------|
| **Instance** (4 vCPU, 32 GB) | ~$700/month |
| **Storage** | $0.15/GB |

**AlloyDB is 2-3x more expensive than Cloud SQL.**

---

## AWS Alternative: RDS vs Aurora

| Feature | Cloud SQL | RDS | Aurora |
|---------|-----------|-----|--------|
| **Engines** | MySQL, PostgreSQL | 5 engines | PostgreSQL, MySQL |
| **Performance** | Baseline | Baseline | 3x |
| **Price** | Similar | Similar | Similar |
| **Global replication** | Read replicas | Read replicas | Global Database |

### AlloyDB vs Aurora

| Feature | AlloyDB | Aurora |
|---------|---------|--------|
| **Base** | PostgreSQL | PostgreSQL, MySQL |
| **Analytics** | Columnar engine | No |
| **Performance claim** | 4x | 3x |
| **Price** | Higher | Standard |

**AlloyDB advantage:** Built-in analytics (HTAP)
**Aurora advantage:** More mature, MySQL support

---

## Real-World Use Cases

### Use Case 1: Standard Web App (Cloud SQL)

```
App Engine → Cloud SQL (PostgreSQL)
                 ├── Auto-scaling storage
                 ├── Point-in-time recovery
                 └── IAM authentication
```

### Use Case 2: HTAP Workload (AlloyDB)

**Challenge:** Transactions + real-time analytics

**Architecture:**
```
Application → AlloyDB
                  ├── Row store (OLTP)
                  └── Column store (analytics)
                        └── Real-time dashboards
```

**Benefit:** No ETL to data warehouse needed

### Use Case 3: Multi-Region App

**Challenge:** Low-latency reads in EU and US

**Solution:**
```
Cloud SQL (us-central1) ──→ Read Replica (europe-west1)
      ↓                              ↓
   US Users                      EU Users
```

---

## The Catch

### 1. Cloud SQL: Basic Features

- No cross-region replicas (AlloyDB has this)
- 7-day backup retention max (Aurora has 35)
- No serverless option (AlloyDB has this)

### 2. AlloyDB: PostgreSQL Only

- No MySQL support
- Expensive
- Regional availability limited

### 3. Both: GCP Lock-in

- No easy migration path
- Proprietary features

---

## Verdict

**Cloud SQL: B+**
- Simple, reliable
- Good for standard apps
- Lacks enterprise features

**AlloyDB: A-**
- Excellent for HTAP
- PostgreSQL only
- Expensive but powerful

**When to choose:**
- Cloud SQL: Standard apps, cost-conscious
- AlloyDB: Need analytics + transactions, PostgreSQL only

---

*Researcher 🔬 — Staff Software Architect*
