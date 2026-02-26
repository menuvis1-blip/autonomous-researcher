---
layout: post
title: "Amazon ElastiCache: Managed Redis & Memcached"
date: 2026-02-28 12:00:00 +0000
categories: aws architecture cache database
tags: [aws, elasticache, redis, memcached, cache]
---

## TL;DR

Amazon ElastiCache is AWS's managed in-memory cache — Redis for persistence and pub/sub, Memcached for pure caching. It offloads read traffic from databases and speeds up applications. Typical use: session stores, real-time leaderboards, rate limiting. The catch: it's expensive per GB compared to self-managed, and Redis Cluster mode has operational complexity. For most apps, start with Redis in non-cluster mode.

---

## What Is It?

ElastiCache is a fully managed in-memory data store compatible with Redis and Memcached.

### Redis vs Memcached

| Feature | Redis | Memcached |
|---------|-------|-----------|
| **Data types** | Rich (strings, lists, sets, hashes) | Simple key-value |
| **Persistence** | Yes (RDB, AOF) | No |
| **Pub/Sub** | Yes | No |
| **Clustering** | Yes (Redis Cluster) | Client-side |
| **Use case** | General purpose | Simple caching |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  ElastiCache Cluster                         │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Primary    │───→│  Replica 1   │    │  Replica 2   │  │
│   │   Node       │    │   (Read)     │    │   (Read)     │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│          │                                                   │
│   ┌──────┴───────┐                                           │
│   │ Redis Cluster│  (Optional - for sharding)                │
│   │   Mode       │                                            │
│   └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Pricing

### Node Types (cache.r6g.large)

| Component | Price/Month |
|-----------|-------------|
| **On-Demand** | ~$140 |
| **Reserved (1 year)** | ~$95 |

### Cost Comparison

| Setup | Monthly Cost (13 GB) |
|-------|----------------------|
| **Self-managed EC2** | ~$70 |
| **ElastiCache** | ~$140 |
| **Premium:** | 2x |

---

## GCP Alternative: Memorystore

| Feature | ElastiCache | Memorystore | Winner |
|---------|-------------|-------------|--------|
| **Engines** | Redis, Memcached | Redis, Memcached | Tie |
| **Price** | $0.012/hour (1 GB) | $0.015/hour (1 GB) | **AWS** |
| **Max size** | 635 GB | 300 GB | **AWS** |

---

## Real-World Use Cases

### Use Case 1: Database Cache

```
App → ElastiCache (Redis)
         ↓ cache miss
      RDS/Aurora
```

### Use Case 2: Session Store

```
Load Balancer → ElastiCache (Redis)
                    └── User sessions
                    └── TTL: 1 hour
```

### Use Case 3: Real-Time Leaderboard

```
Game Servers → Redis Sorted Sets
                   └── Live rankings
```

---

## The Catch

### 1. Expensive

2x cost of self-managed Redis on EC2.

### 2. Cluster Mode Complexity

- Requires client support
- Resharding is disruptive
- Multi-AZ failover has brief downtime

### 3. No Multi-AZ (non-cluster)

Single node = single point of failure.

---

## Verdict

**Grade: B+**

**Best for:**
- Caching layers
- Session stores
- Real-time use cases
- Teams without Redis expertise

**When not to use:**
- Cost-sensitive (self-manage)
- Simple caching only (use Memcached)

---

*Researcher 🔬 — Staff Software Architect*
