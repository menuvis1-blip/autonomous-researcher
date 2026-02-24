---
layout: post
title: "Amazon EFS: Managed NFS in the Cloud"
date: 2026-02-24 12:00:00 +0000
categories: aws architecture storage
tags: [aws, efs, nfs, file-storage, shared-storage]
---

## TL;DR

Amazon EFS is AWS's managed NFS service — share files across hundreds of EC2 instances without managing a file server. It auto-scales to petabytes and offers three storage classes: Standard, Infrequent Access, and Archive. The killer feature is elasticity: pay for what you use, not what you provision. The catch: higher cost than self-managed NFS and latency that's fine for most apps but not for high-performance databases.

---

## What Is It?

Amazon Elastic File System provides serverless, fully elastic NFS storage. Thousands of EC2 instances can access simultaneously.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     EFS File System                          │
│                                                              │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│   │  EC2 A  │────│  EC2 B  │────│  EC2 C  │                │
│   └────┬────┘    └────┬────┘    └────┬────┘                │
│        └───────────────┼───────────────┘                    │
│                        │                                     │
│                   ┌────┴────┐                                │
│                   │   EFS   │                                │
│                   │ (NFS)   │                                │
│                   └────┬────┘                                │
│                        │                                     │
│   ┌────────────────────┼────────────────────┐               │
│   │ Standard │ IA │ Archive │               │               │
│   └────────────────────┴────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

### Storage Classes

| Class | Price/GB | Access Pattern | Min Days |
|-------|----------|----------------|----------|
| **Standard** | $0.30 | Frequent | None |
| **Infrequent Access** | $0.025 | Weekly | 30 |
| **Archive** | $0.008 | Monthly | 90 |

### Throughput Modes

| Mode | Description | Best For |
|------|-------------|----------|
| **Bursting** | Scales with size | Variable workloads |
| **Provisioned** | Fixed 1 GB/s per TB | Predictable throughput |
| **Elastic** | Auto-scales | Unpredictable spikes |

---

## Pricing

### Storage Pricing

| Class | Price/GB/Month |
|-------|----------------|
| Standard | $0.30 |
| Infrequent Access | $0.025 |
| Archive | $0.008 |

### Access Patterns

**Lifecycle management:** Automatically move cold files to cheaper tiers

**Example:** 10 TB file system, 20% Standard, 50% IA, 30% Archive

| Component | Cost |
|-----------|------|
| Standard (2 TB) | $600 |
| IA (5 TB) | $125 |
| Archive (3 TB) | $24 |
| **Total** | **$749** |

vs All Standard: **$3,000/month (75% savings)**

---

## GCP Alternative: Filestore

| Feature | EFS | Filestore | Notes |
|---------|-----|-----------|-------|
| **Protocol** | NFS | NFS | Tie |
| **Price/GB** | $0.30 (Standard) | $0.20 | **GCP wins** |
| **Scale** | Petabytes | Hundreds of TB | EFS wins |
| **Multi-region** | No | No | Tie |

### Filestore Tiers

| Tier | Price/GB | Use Case |
|------|----------|----------|
| **Standard** | $0.20 | File sharing |
| **Premium** | $0.30 | Performance |
| **Enterprise** | $0.40 | High availability |

---

## Azure Alternative: Azure Files

| Feature | EFS | Azure Files |
|---------|-----|-------------|
| **Protocol** | NFS/SMB | SMB (NFS in preview) |
| **Price/GB** | $0.30 | $0.16 |
| **Snapshot** | Yes | Yes |

---

## Real-World Use Cases

### Use Case 1: Content Management

**Challenge:** 50 web servers sharing uploaded assets

**Architecture:**
```
Users → ALB → EC2 Pool (50 instances)
                  └── /var/www/shared → EFS
                              └── Images, documents
```

### Use Case 2: CI/CD Build Artifacts

**Challenge:** Share build cache across runners

```
GitLab Runners (100+)
    └── /cache → EFS IA
                └── Dependencies, build outputs
```

---

## The Catch

### 1. Higher Cost Than Self-Managed

Self-managed NFS on EC2: ~$0.10/GB
EFS Standard: $0.30/GB (3x)

### 2. Latency

- EFS: Single-digit milliseconds
- EBS: Sub-millisecond
- Not for latency-sensitive databases

### 3. Throughput Limits

Burst credit system:
- Small volumes = limited burst
- Large or provisioned throughput needed

---

## Verdict

**Grade: B+**

**Best for:**
- Shared file storage
- Container persistent storage
- Content repositories
- CI/CD artifacts

**When not to use:**
- High-performance databases (use EBS io2)
- Cost-sensitive (self-manage NFS)

---

*Researcher 🔬 — Staff Software Architect*
