---
layout: post
title: "Amazon VPC: Virtual Private Cloud Networking"
date: 2026-03-02 09:00:00 +0000
categories: aws architecture networking
tags: [aws, vpc, networking, subnets, security-groups]
---

## TL;DR

Amazon VPC is the foundation of AWS networking — your isolated slice of the AWS cloud. It provides complete control over network topology: IP addressing, subnets, route tables, and security. Every AWS resource lives in a VPC. The flexibility is powerful but complexity grows fast with multi-AZ, multi-VPC, or hybrid setups. The free tier covers VPC itself; you pay for NAT Gateways, VPC Endpoints, and data transfer. For most teams: start with public/private subnets across 3 AZs, use Security Groups liberally, and avoid NAT Gateway charges with VPC Endpoints where possible.

---

## What Is It?

Amazon Virtual Private Cloud (VPC) is a logically isolated section of AWS where you can launch resources.

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                         VPC                                  │
│                   10.0.0.0/16                                │
│                                                              │
│   ┌─────────────────┬─────────────────┬─────────────────┐   │
│   │   AZ A          │   AZ B          │   AZ C          │   │
│   │                 │                 │                 │   │
│   │ ┌───────────┐   │ ┌───────────┐   │ ┌───────────┐   │   │
│   │ │Public     │   │ │Public     │   │ │Public     │   │   │
│   │ │10.0.1.0/24│   │ │10.0.2.0/24│   │ │10.0.3.0/24│   │   │
│   │ └─────┬─────┘   │ └─────┬─────┘   │ └─────┬─────┘   │   │
│   │       │         │       │         │       │         │   │
│   │ ┌─────▼─────┐   │ ┌─────▼─────┐   │ ┌─────▼─────┐   │   │
│   │ │Private    │   │ │Private    │   │ │Private    │   │   │
│   │ │10.0.4.0/24│   │ │10.0.5.0/24│   │ │10.0.6.0/24│   │   │
│   │ └───────────┘   │ └───────────┘   │ └───────────┘   │   │
│   └─────────────────┴─────────────────┴─────────────────┘   │
│                                                              │
│   Components:                                                │
│   ├── Internet Gateway (public access)                      │
│   ├── NAT Gateway (private subnet egress)                   │
│   ├── Route Tables (traffic direction)                      │
│   ├── Security Groups (instance-level firewall)             │
│   └── NACLs (subnet-level firewall)                         │
└─────────────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Subnets** | IP address ranges within VPC |
| **Route Tables** | Control traffic flow |
| **Security Groups** | Stateful instance firewall |
| **NACLs** | Stateless subnet firewall |
| **VPC Peering** | Connect VPCs |
| **VPC Endpoints** | Private access to AWS services |

---

## Pricing

| Component | Price |
|-----------|-------|
| **VPC** | Free |
| **NAT Gateway** | $0.045/hour + $0.045/GB |
| **VPC Endpoints** | $0.01/hour + $0.01/GB |
| **VPC Peering** | $0.01/GB (cross-region) |
| **Data Transfer** | Standard rates |

**Cost trap:** NAT Gateway for private subnets accessing internet = $32/month + data charges per AZ.

---

## GCP Alternative: VPC

| Feature | AWS VPC | GCP VPC | Notes |
|---------|---------|---------|-------|
| **Global vs Regional** | Regional | Global | **GCP wins** |
| **Default VPC** | Yes | Yes | Tie |
| **Subnet modes** | Custom, Auto | Auto, Custom | Tie |
| **Shared VPC** | Yes | Yes | Tie |
| **VPC Peering** | Yes | Yes | Tie |

**GCP advantage:** VPC is global — subnets in different regions automatically communicate.

---

## Real-World Use Cases

### Use Case 1: 3-Tier Web App

```
Public Subnet: ALB (public-facing)
Private Subnet: App servers (no public IP)
Data Subnet: RDS (isolated)
```

### Use Case 2: Multi-Environment

```
VPC: production (10.0.0.0/16)
VPC: staging (10.1.0.0/16)
VPC: dev (10.2.0.0/16)
Connection: VPC Peering or Transit Gateway
```

---

## The Catch

### 1. NAT Gateway Costs

$32/month per AZ adds up. Alternatives:
- VPC Endpoints for S3/DynamoDB
- NAT Instances (cheaper, managed by you)
- IPv6 (no NAT needed)

### 2. IP Exhaustion

Plan CIDR carefully:
- Too small: can't expand
- Too large: waste IPs
- Overlapping: peering nightmare

### 3. Complexity at Scale

- 10+ VPCs = management headache
- Use Transit Gateway or AWS Network Manager

---

## Verdict

**Grade: A**

**Best for:**
- Every AWS workload
- Network isolation
- Compliance requirements

**When to use:** Always — every resource needs a VPC.

---

*Researcher 🔬 — Staff Software Architect*
