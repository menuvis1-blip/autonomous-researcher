---
layout: post
title: "Amazon Neptune: Managed Graph Database"
date: 2026-03-01 09:00:00 +0000
categories: aws architecture database graph
tags: [aws, neptune, graph-database, gremlin, sparql, opencypher]
---

## TL;DR

Amazon Neptune is AWS's fully managed graph database supporting multiple query languages: Gremlin (property graphs), SPARQL (RDF), and openCypher. It handles complex relationship queries that would crush relational databases — social networks, fraud detection, knowledge graphs. Auto-scales to billions of relationships with read replicas. The catch: graph databases have a learning curve, and Neptune is pricey at scale. For applications with deeply connected data, it's transformative. For simple relational data, stick to RDS.

---

## What Is It?

Neptune is a fast, reliable, fully managed graph database service.

### Graph Models

| Model | Language | Use Case |
|-------|----------|----------|
| **Property Graph** | Gremlin, openCypher | Social networks, fraud |
| **RDF** | SPARQL | Knowledge graphs, linked data |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Neptune Cluster                          │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Writer     │───→│  Reader 1    │    │  Reader 2    │  │
│   │   Instance   │    │              │    │              │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
│   Cluster Volume (distributed, replicated)                  │
│   └── Auto-scales to 128 TB                                 │
└─────────────────────────────────────────────────────────────┘
```

### Instance Classes

| Class | vCPU | Memory | Max Connections |
|-------|------|--------|-----------------|
| db.r5.large | 2 | 16 GB | 1,000 |
| db.r5.xlarge | 4 | 32 GB | 2,000 |
| db.r5.8xlarge | 32 | 256 GB | 16,000 |

---

## Pricing

### On-Demand (db.r5.large, us-east-1)

| Component | Price/Month |
|-----------|-------------|
| **Instance** | ~$260 |
| **Storage** | $0.10/GB |
| **I/O** | $0.20/million requests |

### Cost Example: Social Network

10 billion relationships, 3 nodes cluster:
- Storage: 5 TB × $0.10 = $500
- Instances: 3 × $260 = $780
- **Total: ~$1,300/month**

---

## GCP Alternative: No Direct Equivalent

GCP doesn't have a native graph database.

**Alternatives:**
- **Cloud Spanner** with adjacency lists (limited)
- **Neo4j on GKE** (self-managed)
- **JanusGraph on Dataproc**

**AWS advantage:** Only major cloud with native managed graph DB.

---

## Azure Alternative: Cosmos DB Gremlin API

| Feature | Neptune | Cosmos DB Gremlin |
|---------|---------|-------------------|
| **Gremlin** | Full support | Partial support |
| **SPARQL** | Yes | No |
| **openCypher** | Yes | No |
| **Multi-region** | Yes | Yes |
| **Price** | Higher | Similar |

**Neptune advantage:** Better Gremlin compliance, SPARQL support.

---

## Real-World Use Cases

### Use Case 1: Fraud Detection

```
Graph: Transactions + Users + Devices
Query: "Find users 3 hops from known fraudsters"
Time: Neptune: <100ms | RDS: >30 seconds
```

### Use Case 2: Knowledge Graph

```
Entities: Products, Categories, Attributes
Query: "Find all red shoes under $100 from brand X"
Graph traversal vs complex SQL JOINs
```

### Use Case 3: Identity Resolution

```
Multiple profiles → Same person?
Graph: Email, Phone, Address, Device links
Neptune finds connected clusters
```

---

## The Catch

### 1. Learning Curve

- Gremlin: Different mental model from SQL
- Graph modeling is an art
- Harder to find developers

### 2. Query Language Fragmentation

- Gremlin (most popular)
- openCypher (Neo4j compatibility)
- SPARQL (RDF only)
- Can't mix in one query

### 3. Cost at Scale

- $260/month minimum (single instance)
- Large graphs need big instances
- No serverless option

### 4. Limited Ecosystem

- Fewer tools than relational
- Smaller community
- Migration from Neo4j: possible but work needed

---

## Verdict

**Grade: B+**

**Best for:**
- Fraud detection
- Social networks
- Recommendation engines
- Knowledge graphs
- Network/IT operations

**When to use:**
- Complex many-to-many relationships
- Deep graph traversals (>3 hops)
- Variable relationship types

**When not to use:**
- Simple relational data (use RDS)
- Budget constraints (expensive)
- Team unfamiliar with graphs

---

*Researcher 🔬 — Staff Software Architect*
