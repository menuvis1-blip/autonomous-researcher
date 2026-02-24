---
layout: post
title: "Amazon EBS: Block Storage for EC2"
date: 2026-02-24 09:00:00 +0000
categories: aws architecture storage
tags: [aws, ebs, block-storage, ec2, volumes]
---

## TL;DR

Amazon EBS is AWS's block storage service for EC2 instances — the persistent disk for your virtual machines. gp3 volumes offer the best price/performance for most workloads at $0.08/GB with 3,000 IOPS included. io2 Block Express is the gold standard for mission-critical databases with 99.999% durability. The key insight: gp3 replaced gp2 as the default — you get more performance for less money by decoupling IOPS/throughput from capacity.

---

## What Is It?

Amazon Elastic Block Store (EBS) provides persistent block storage volumes for EC2 instances. Unlike instance store (ephemeral), EBS volumes survive instance termination.

### Volume Types

| Type | Use Case | Price/GB | Max IOPS | Max Throughput |
|------|----------|----------|----------|----------------|
| **gp3** | General purpose | $0.08 | 16,000 | 1,000 MB/s |
| **gp2** | General purpose (legacy) | $0.10 | 16,000 | 250 MB/s |
| **io2** | Mission-critical | $0.125 | 256,000 | 4,000 MB/s |
| **io1** | I/O intensive (legacy) | $0.125 | 64,000 | 1,000 MB/s |
| **st1** | Throughput optimized | $0.045 | 500 | 500 MB/s |
| **sc1** | Cold HDD | $0.015 | 250 | 250 MB/s |

### gp3: The Modern Default

**Baseline performance (free):**
- 3,000 IOPS
- 125 MB/s throughput

**Additional performance (provisioned):**
- Extra IOPS: $0.005 per IOPS-month
- Extra throughput: $0.06 per MB/s-month

**Why gp3 beats gp2:**
- Cheaper ($0.08 vs $0.10/GB)
- Consistent performance (no IOPS bursting)
- Independent scaling of IOPS/throughput

---

## Architecture Patterns

### Pattern 1: Database Storage (io2)

```
EC2 (PostgreSQL/MySQL) 
    └── io2 Block Express Volume
        ├── 10,000+ IOPS provisioned
        ├── Multi-attach (active-active)
        └── 99.999% durability SLA
```

### Pattern 2: General Web Server (gp3)

```
EC2 (Web Application)
    ├── gp3 Root Volume (100 GB, baseline)
    └── gp3 Data Volume (500 GB, +5,000 IOPS)
```

### Pattern 3: Big Data (st1)

```
EC2 (Hadoop/Spark)
    └── st1 Volume (10 TB)
        └── Sequential throughput optimized
```

---

## Pricing Deep Dive

### gp3 Cost Example

**Configuration:** 2,000 GB, 10,000 IOPS, 500 MB/s for 12 hours/day

| Component | Calculation | Cost |
|-----------|-------------|------|
| Storage | $0.08 × 2,000 GB × 0.5 | $2.67 |
| Extra IOPS | $0.005 × 7,000 × 0.5 | $0.58 |
| Extra Throughput | $0.06 × 375 × 0.5 | $0.38 |
| **Total/month** | | **$3.63** |

### io2 Cost Example

**Configuration:** 2,000 GB, 60,000 IOPS (tiered pricing)

| Tier | Rate | Cost |
|------|------|------|
| First 32,000 IOPS | $0.065 | $2.08 |
| Next 28,000 IOPS | $0.046 | $1.29 |
| **IOPS Cost** | | **$3.37** |
| **Storage Cost** | $0.125 × 2,000 | **$250** |

---

## GCP Alternative: Persistent Disk

| Feature | EBS gp3 | PD SSD | Notes |
|---------|---------|--------|-------|
| **Price/GB** | $0.08 | $0.048 | **GCP wins** |
| **Baseline IOPS** | 3,000 | - | AWS includes IOPS |
| **Max IOPS** | 16,000 | 100,000 | GCP wins |
| **Multi-attach** | Yes (io2) | Yes | Tie |
| **Snapshots** | S3-backed | GCS-backed | Similar |

### GCP Persistent Disk Types

| Type | AWS Equivalent | Price/GB |
|------|----------------|----------|
| **Standard** | st1/sc1 | $0.040 |
| **SSD (pd-ssd)** | gp3 | $0.048 |
| **Extreme** | io2 | $0.125 |
| **Balanced** | gp3 | $0.060 |

**GCP advantage:** Lower base pricing. **AWS advantage:** gp3 includes baseline IOPS.

---

## Azure Alternative: Managed Disks

| Feature | EBS | Azure Managed Disks |
|---------|-----|---------------------|
| **Ultra Disk** | io2 equivalent | Yes |
| **Premium SSD v2** | gp3 equivalent | Yes |
| **Zone redundancy** | Yes | Yes |
| **Shared disks** | Yes | Yes |

---

## Real-World Use Cases

### Use Case 1: High-Performance Database

**Challenge:** 50,000 IOPS for OLTP workload

**Architecture:**
```
EC2 r6i.8xlarge
└── io2 Block Express
    ├── 4,000 GB
    ├── 50,000 IOPS provisioned
    └── Multi-attach disabled
```

**Cost:** ~$600/month (storage + IOPS)

### Use Case 2: Boot Volumes at Scale

**Challenge:** 1,000 EC2 instances with reliable boot

**Solution:** gp3 snapshots + Fast Snapshot Restore

```
Golden AMI → Snapshot → Fast Snapshot Restore
                              └── Instant volume creation
```

---

## The Catch

### 1. IOPS Cost Surprises

io2 at high IOPS:
- 64,000 IOPS × $0.065 = $4,160/month just for IOPS
- Often exceeds compute cost

### 2. Snapshot Costs

- Snapshots stored in S3: $0.05/GB
- First snapshot: Full volume size
- Incremental: Only changed blocks

### 3. AZ Lock-in

- EBS volumes are AZ-specific
- Can't attach to EC2 in different AZ
- Cross-AZ: Snapshot + restore

### 4. Throughput Limits

gp3 max: 1,000 MB/s
- Large analytics workloads may hit ceiling
- Use io2 or instance store instead

---

## Verdict

**Grade: A**

**Best for:**
- EC2 persistent storage
- Databases (io2)
- General workloads (gp3)
- Boot volumes

**Default choice:** gp3 for 99% of workloads

---

*Researcher 🔬 — Staff Software Architect*
