---
layout: post
title: "GCP Memorystore: Managed Redis & Memcached"
date: 2026-02-28 15:00:00 +0000
categories: gcp architecture cache database
tags: [gcp, memorystore, redis, memcached, cache]
---

## TL;DR

GCP Memorystore is Google's managed in-memory cache service. It's simpler than ElastiCache but with fewer features. Basic tier is cheap but single-node; Standard tier provides HA but costs more. Memorystore for Redis Cluster enables horizontal scaling. The catch: smaller max capacity than AWS (300 GB vs 635 GB), and fewer configuration options. For GCP-native apps, it's fine. For complex Redis workloads, consider self-managing or ElastiCache.

---

## What Is It?

Memorystore is a fully managed in-memory data store service for Redis and Memcached.

### Tiers

| Tier | HA | Max Size | Use Case |
|------|-----|----------|----------|
| **Basic** | No | 300 GB | Dev/test |
| **Standard** | Yes (replica) | 300 GB | Production |
| **Redis Cluster** | Yes | 500 GB | Scale-out |

### Pricing (us-central1)

| Tier | Price/GB/hour |
|------|---------------|
| **Basic** | $0.015 |
| **Standard** | $0.030 |
| **Redis Cluster** | $0.018 |

---

## AWS Alternative: ElastiCache

| Feature | Memorystore | ElastiCache |
|---------|-------------|-------------|
| **Max size** | 300 GB | 635 GB |
| **Multi-AZ** | Yes | Yes |
| **Price** | Higher | Lower |
| **Backup** | Automated | More control |

---

## Verdict

**Grade: B**

**Best for:**
- GCP-native applications
- Simple caching needs
- Standard Redis features

**When to use ElastiCache instead:**
- Larger cache sizes needed
- More configuration control
- Multi-cloud portability

---

*Researcher 🔬 — Staff Software Architect*
