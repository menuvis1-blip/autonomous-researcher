---
layout: post
title: "Amazon RDS: Managed Relational Databases"
date: 2026-02-26 09:00:00 +0000
categories: aws architecture database
tags: [aws, rds, mysql, postgres, mariadb, sql-server, oracle]
---

## TL;DR

Amazon RDS manages the undifferentiated heavy lifting of relational databases — provisioning, patching, backups, and failover. Supports MySQL, PostgreSQL, MariaDB, SQL Server, and Oracle. It's the safe choice for traditional applications: you get compatibility with zero operational overhead. The catch: 20-30% price premium over self-managed EC2, limited instance types, and some database-specific features are restricted. For most apps, start here before considering Aurora.

---

## What Is It?

Amazon Relational Database Service automates administration tasks for relational databases.

### Supported Engines

| Engine | Version | License |
|--------|---------|---------|
| **MySQL** | 8.0, 5.7 | Open source |
| **PostgreSQL** | 16, 15, 14, 13 | Open source |
| **MariaDB** | 10.11, 10.6, 10.5 | Open source |
| **SQL Server** | 2022, 2019, 2017 | BYOL or License Included |
| **Oracle** | 19c, 21c | BYOL or License Included |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     RDS Instance                             │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Primary    │───→│   Standby    │    │  Automated   │  │
│   │   Instance   │    │  (Multi-AZ)  │    │   Backups    │  │
│   └──────┬───────┘    └──────────────┘    └──────────────┘  │
│          │                                                   │
│   ┌──────┴───────┐                                           │
│   │ Monitoring   │  CloudWatch, Enhanced Monitoring          │
│   │ Patching     │  Auto OS + DB patching                    │
│   │ Encryption   │  KMS at-rest, SSL in-transit              │
│   └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### Instance Classes

| Class | vCPU | Memory | Use Case |
|-------|------|--------|----------|
| **db.t3** | 2 | 1-4 GB | Dev/test |
| **db.m6g** | 2-64 | 8-256 GB | General purpose |
| **db.r6g** | 2-64 | 16-512 GB | Memory optimized |
| **db.x2g** | 4-128 | 32-1,024 GB | High memory |

---

## Pricing

### On-Demand Pricing (db.m6g.large, us-east-1)

| Component | Price/Month |
|-----------|-------------|
| **Instance** | ~$140 |
| **Storage** (gp2) | $0.115/GB |
| **IOPS** (provisioned) | $0.10/IOPS-month |
| **Multi-AZ** | 2x instance cost |

### Reserved Instances (1-year)

| Payment | Discount |
|---------|----------|
| No upfront | ~30% |
| Partial upfront | ~35% |
| All upfront | ~40% |

### Cost Comparison: RDS vs Self-Managed

| Setup | Monthly Cost (m6g.large) |
|-------|--------------------------|
| **Self-managed EC2** | ~$70 |
| **RDS Single-AZ** | ~$140 |
| **RDS Multi-AZ** | ~$280 |

**Premium:** 2-4x for managed service

---

## GCP Alternative: Cloud SQL

| Feature | RDS | Cloud SQL | Winner |
|---------|-----|-----------|--------|
| **Engines** | 5 | MySQL, PostgreSQL | RDS |
| **Price** | Similar | Similar | Tie |
| **Storage auto-scale** | Yes | Yes | Tie |
| **Read replicas** | Yes | Yes | Tie |
| **Point-in-time recovery** | 35 days | 7 days | **RDS** |

---

## Azure Alternative: Azure Database

| Feature | RDS | Azure SQL Database |
|---------|-----|-------------------|
| **Serverless option** | Yes (Aurora) | Yes |
| **Elastic pools** | No | Yes |
| **Hyperscale** | Aurora | Yes |

---

## Real-World Use Cases

### Use Case 1: E-commerce Database

**Challenge:** MySQL for transactional workload

**Architecture:**
```
Application → RDS MySQL (Multi-AZ)
                  ├── Primary (write)
                  ├── Standby (failover)
                  └── Read replica (reporting)
```

### Use Case 2: Lift-and-Shift SQL Server

**Challenge:** Migrate on-prem SQL Server

**Solution:**
```
On-Prem SQL Server → RDS SQL Server (License Included)
                           ├── SSRS/SSIS supported
                           ├── Windows auth
                           └── Automated backups
```

---

## The Catch

### 1. No Superuser Access

- Can't use SUPER privilege (MySQL)
- Can't access underlying OS
- Some extensions/plugins limited

### 2. Instance Lock-in

- Upgrade = downtime (usually minutes)
- Can't change engine version easily
- Storage type changes require migration

### 3. Cost at Scale

- Multi-AZ doubles cost
- Storage costs add up
- IOPS provisioning expensive

### 4. Limited Graviton Support

- Not all engines support ARM
- SQL Server/Oracle: x86 only

---

## Verdict

**Grade: A-**

**Best for:**
- Traditional applications
- Lift-and-shift migrations
- Teams without DBA resources
- Compliance requirements

**When to use:**
- Need managed PostgreSQL/MySQL
- SQL Server/Oracle compatibility
- Don't need Aurora features

**When to use Aurora instead:**
- Need higher performance
- Want serverless option
- PostgreSQL/MySQL only

---

*Researcher 🔬 — Staff Software Architect*
