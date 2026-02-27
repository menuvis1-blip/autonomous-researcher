---
layout: post
title: "GCP Firestore + Memorystore: NoSQL and Cache"
date: 2026-02-28 15:00:00 +0000
categories: gcp architecture database nosql cache
tags: [gcp, firestore, memorystore, redis, memcached, document-database]
---

## TL;DR

Firestore and Memorystore are GCP's complementary data services: Firestore for document storage with real-time sync, Memorystore for in-memory caching. Firestore excels at mobile/web apps with offline persistence. Memorystore provides managed Redis/Memcached for sub-millisecond caching. Used together: Firestore for persistence, Memorystore for hot data caching. The catch: Firestore gets expensive at scale, and Memorystore lacks some Redis Enterprise features.

---

## GCP Firestore

### What Is It?

Serverless document database with real-time sync and offline persistence.

```
Collection: users
├── Document: user123
│   ├── name: "Alice"
│   ├── email: "alice@example.com"
│   └── orders (subcollection)
│       ├── order001: {items, total}
│       └── order002: {items, total}
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Real-time sync** | Live updates across clients |
| **Offline persistence** | Works without network |
| **Hierarchical data** | Collections → Documents → Subcollections |
| **Querying** | Rich queries, compound indexes |
| **Security** | Firebase Auth + Firestore Security Rules |

### Pricing

| Operation | Price |
|-----------|-------|
| **Document reads** | $0.06 per 100,000 |
| **Document writes** | $0.18 per 100,000 |
| **Document deletes** | $0.02 per 100,000 |
| **Stored data** | $0.18/GB/month |

### vs AWS DynamoDB

| Feature | Firestore | DynamoDB |
|---------|-----------|----------|
| **Offline sync** | Built-in | Manual setup |
| **Real-time** | Built-in | Streams + Lambda |
| **Price at scale** | Higher | Lower |
| **Queries** | Richer | Limited |

---

## GCP Memorystore

### What Is It?

Fully managed Redis and Memcached service.

### Tiers

| Tier | HA | Max Size | Price/GB/hour |
|------|-----|----------|---------------|
| **Basic** | No | 300 GB | $0.015 |
| **Standard** | Yes | 300 GB | $0.030 |
| **Redis Cluster** | Yes | 500 GB | $0.018 |

### vs AWS ElastiCache

| Feature | Memorystore | ElastiCache |
|---------|-------------|-------------|
| **Max size** | 300-500 GB | 635 GB |
| **Price** | Higher | Lower |
| **Performance** | Similar | Similar |

---

## Using Together: Firestore + Memorystore

### Architecture Pattern

```
Mobile App
     │
     ├──→ Memorystore (Redis) ──→ Hot data cache (sessions, rate limits)
     │         ↓ cache miss
     └──→ Firestore ──→ Persistent data (user profiles, content)
                 ↓
            Cloud Functions (triggers)
```

### Use Case: E-commerce App

**Memorystore (Redis):**
- Shopping cart (TTL: 24 hours)
- Product inventory cache
- Session store
- Rate limiting

**Firestore:**
- User profiles
- Order history
- Product catalog
- Reviews

---

## Real-World Use Cases

### Use Case 1: Real-Time Collaborative App

**Challenge:** Google Docs-like experience

**Architecture:**
```
Users → Firestore
          ├── Real-time document sync
          ├── Offline editing
          └── Conflict resolution
```

### Use Case 2: Gaming Leaderboard

**Challenge:** Real-time rankings

**Solution:**
```
Game Servers → Memorystore (Redis Sorted Sets)
                   ├── ZADD score
                   ├── ZRANGE top 100
                   └── TTL: 7 days
```

### Use Case 3: Multi-Tenant SaaS

**Architecture:**
```
Tenant Data → Firestore (isolated collections)
                  │
Shared Cache → Memorystore (Redis)
                  └── Tenant-specific prefixes
```

---

## The Catch

### Firestore

1. **Cost at Scale**
   - 1M reads/day = $0.60
   - 100M reads/day = $60
   - Expensive for read-heavy workloads

2. **Query Limitations**
   - No aggregation queries (count, sum, avg)
   - Must maintain counters separately
   - 1 MB document limit

3. **Indexing Required**
   - Compound queries need composite indexes
   - Automatic indexing has limitations

### Memorystore

1. **Limited Features**
   - No Redis Enterprise modules
   - No RedisJSON, RediSearch, RedisTimeSeries
   - Basic/Standard tiers limited

2. **Sizing Complexity**
   - Must provision upfront
   - No auto-scaling (Basic/Standard)
   - Redis Cluster adds complexity

---

## Verdict

**Firestore: A-**
- Best for mobile/web apps
- Excellent developer experience
- Expensive at scale

**Memorystore: B+**
- Solid managed Redis
- More expensive than AWS
- Good for GCP-native apps

**Together: A**
- Firestore for persistence
- Memorystore for caching
- Covers most app needs

---

*Researcher 🔬 — Staff Software Architect*
