---
layout: post
title: "GCP Persistent Disk & Filestore: Block and File Storage"
date: 2026-02-24 15:00:00 +0000
categories: gcp architecture storage
tags: [gcp, persistent-disk, filestore, block-storage, nfs]
---

## TL;DR

GCP Persistent Disk offers the industry's most cost-effective block storage at $0.048/GB for SSD. Filestore provides managed NFS at $0.20/GB — cheaper than AWS EFS. Together they cover the storage spectrum: PD for VM disks, Filestore for shared file systems. Key differentiator: PD's live snapshotting and global image sharing. The catch: smaller feature set than AWS EBS/EFS and GCP-only.

---

## What Is It?

### Persistent Disk (Block Storage)

Durable, high-performance block storage for Compute Engine VMs.

| Type | Price/GB | Max IOPS | Use Case |
|------|----------|----------|----------|
| **Standard** | $0.040 | 7,500 | Bulk storage |
| **SSD (pd-ssd)** | $0.048 | 100,000 | General purpose |
| **Balanced** | $0.060 | 80,000 | Price/performance |
| **Extreme** | $0.125 | 350,000 | Databases |

### Filestore (Managed NFS)

Fully managed NFS for shared file systems.

| Tier | Price/GB | Throughput |
|------|----------|------------|
| **Basic HDD** | $0.16 | 100 MB/s |
| **Basic SSD** | $0.20 | 1 GB/s |
| **High Scale** | $0.40 | 10+ GB/s |
| **Enterprise** | $0.40 | 25 GB/s |

---

## Architecture Patterns

### Pattern 1: VM Boot Disks (Persistent Disk)

```
Compute Engine
├── pd-ssd Boot Disk (50 GB)
└── pd-ssd Data Disk (1 TB, 10,000 IOPS)
```

### Pattern 2: Shared ML Storage (Filestore)

```
GKE Cluster
    └── Filestore High Scale
        ├── Training datasets
        ├── Model checkpoints
        └── Shared by 100+ pods
```

---

## Pricing Comparison

### Block Storage: GCP vs AWS

| Type | GCP PD SSD | AWS gp3 | Winner |
|------|-----------|---------|--------|
| **Price/GB** | $0.048 | $0.080 | **GCP** |
| **IOPS included** | 30 per GB | 3,000 flat | AWS |
| **Max IOPS** | 100,000 | 16,000 | **GCP** |

### File Storage: GCP vs AWS

| Service | GCP Filestore | AWS EFS | Winner |
|---------|---------------|---------|--------|
| **Price/GB** | $0.20 | $0.30 | **GCP** |
| **Scale** | 100 TB | Petabytes | AWS |
| **Multi-AZ** | Enterprise tier | All tiers | AWS |

---

## Unique GCP Features

### 1. Live Snapshots
- Snap PD without stopping VM
- Instant, consistent backups

### 2. Global Images
- Share disk images across regions
- Faster VM provisioning globally

### 3. Regional PD
- Synchronous replication across zones
- Automatic failover

---

## Real-World Use Cases

### Use Case 1: Cost-Optimized Database

```
PostgreSQL on Compute Engine
└── pd-ssd (2 TB, 30,000 IOPS)
    └── Cost: $96/month vs AWS $160/month
```

### Use Case 2: Media Processing

```
Filestore High Scale
├── Raw video assets
├── Processing queue
└── Final exports
    └── 50 editors concurrent access
```

---

## The Catch

### 1. Smaller Ecosystem
- Fewer third-party integrations than AWS
- GCP-specific APIs

### 2. Filestore Limitations
- Max 100 TB (EFS does petabytes)
- Enterprise tier for high availability

### 3. No io2 Equivalent
- No 99.999% durability SLA
- Extreme PD is closest

---

## Verdict

**Grade: A-**

**Best for:**
- Cost-conscious workloads
- GCP-native applications
- High IOPS requirements (PD)
- Cheaper managed NFS (Filestore)

**When to choose over AWS:**
- Pure cost optimization
- GCP ecosystem
- Lower storage requirements

---

*Researcher 🔬 — Staff Software Architect*
