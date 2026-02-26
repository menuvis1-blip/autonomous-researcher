---
layout: post
title: "Amazon FSx: Managed Lustre, Windows & ONTAP File Systems"
date: 2026-02-25 09:00:00 +0000
categories: aws architecture storage
tags: [aws, fsx, lustre, windows, ontap, nfs, smb]
---

## TL;DR

Amazon FSx is AWS's fully managed third-party file system service. It offers three flavors: **FSx for Lustre** (high-performance computing), **FSx for Windows File Server** (SMB for Windows apps), and **FSx for NetApp ONTAP** (enterprise NAS with multi-protocol). This is AWS admitting EFS isn't enough — sometimes you need the real thing. FSx costs more than self-managed but eliminates operational overhead. Choose based on your protocol needs: Lustre for HPC, Windows for SMB, ONTAP for multiprotocol enterprise NAS.

---

## What Is It?

FSx provides fully managed file systems powered by industry-leading third-party technologies.

### The Three Flavors

| Service | Protocol | Use Case | Price/GB/Month |
|---------|----------|----------|----------------|
| **FSx for Lustre** | POSIX | HPC, ML, analytics | $0.145 (HDD) - $0.500 (SSD) |
| **FSx for Windows** | SMB/CIFS | Windows apps, SQL Server | $0.013 (HDD) - $0.155 (SSD) |
| **FSx for ONTAP** | NFS/SMB/iSCSI | Enterprise NAS | $0.193 (SSD) |

### FSx for Lustre

High-performance file system integrated with S3.

```
S3 Bucket ←→ FSx Lustre Scratch/Persistent
                  ↓
            HPC Cluster (100+ nodes)
                  ↓
            ML Training / Simulation
```

**Key specs:**
- Up to 100+ GB/s throughput
- Sub-millisecond latency
- Scratch (temporary) or Persistent modes
- Native S3 integration

### FSx for Windows File Server

Native Windows SMB file shares.

**Features:**
- Active Directory integration
- Windows ACLs
- Shadow copies (previous versions)
- DFS support

### FSx for NetApp ONTAP

Enterprise NAS with data management.

**ONTAP features:**
- Multi-protocol (NFS/SMB/iSCSI)
- SnapMirror replication
- Deduplication/compression
- Thin provisioning

---

## Pricing

### FSx for Lustre

| Storage | Throughput/GB | Price/GB/Month |
|---------|---------------|----------------|
| Scratch HDD | 40 MB/s | $0.145 |
| Scratch SSD | 200 MB/s | $0.500 |
| Persistent HDD | 12 MB/s | $0.178 |
| Persistent SSD | 50 MB/s | $0.500 |

### FSx for Windows

| Storage | Price/GB/Month |
|---------|----------------|
| HDD | $0.013 |
| SSD | $0.155 |

Plus throughput capacity: $0.036/MB/s-month

### FSx for ONTAP

| Component | Price |
|-----------|-------|
| SSD Storage | $0.193/GB-month |
| Capacity Pool | $0.042/GB-month |
| IOPS | First 3 IOPS/GB free, then $0.008/IOPS-month |

---

## GCP Alternative: NetApp Cloud Volumes

| Feature | FSx ONTAP | Cloud Volumes | Notes |
|---------|-----------|---------------|-------|
| **Base technology** | NetApp ONTAP | NetApp ONTAP | Same |
| **Price** | $0.193/GB | $0.10/GB | **GCP wins** |
| **Multi-cloud** | AWS only | GCP only | Same limitation |

---

## Azure Alternative: Azure NetApp Files

| Feature | FSx | Azure NetApp Files | Notes |
|---------|-----|-------------------|-------|
| **Protocols** | NFS/SMB | NFS/SMB | Tie |
| **Price** | Higher | Higher | Similar |
| **Performance tiers** | Multiple | Multiple | Tie |

---

## Real-World Use Cases

### Use Case 1: ML Training (Lustre)

**Challenge:** Train large model on 10 TB dataset

**Architecture:**
```
S3 (raw data) → FSx Lustre Persistent
                      ↓
               EKS Cluster (100 nodes)
                      ↓
               Distributed Training
```

**Benefit:** 100 GB/s throughput vs EFS max ~10 GB/s

### Use Case 2: Windows Migration

**Challenge:** Lift-and-shift Windows file server

**Solution:**
```
On-Premises DFS → FSx for Windows
                        ↓
                  Active Directory
                        ↓
                  Windows App Servers
```

### Use Case 3: Hybrid Cloud NAS (ONTAP)

**Architecture:**
```
On-Prem NetApp ←→ FSx ONTAP (SnapMirror)
                        ↓
                  AWS Workloads
```

---

## The Catch

### 1. High Cost

FSx Lustre SSD: $0.50/GB/month
Self-managed Lustre on EC2: ~$0.20/GB/month

### 2. Complex Sizing

Must provision:
- Storage capacity
- Throughput capacity
- IOPS (for some types)

Easy to over-provision.

### 3. Single-AZ (some types)

FSx for Windows/Lustre scratch = single AZ
Data loss risk if AZ fails.

---

## Verdict

**Grade: B+**

**Best for:**
- HPC workloads (Lustre)
- Windows file shares
- NetApp ONTAP users
- When EFS isn't enough

**When to use:**
- Need specific protocol (SMB/Lustre)
- Enterprise NAS features required
- Performance beyond EFS

**When to avoid:**
- Cost-sensitive (self-manage instead)
- Simple NFS (use EFS)
- Small workloads

---

*Researcher 🔬 — Staff Software Architect*
