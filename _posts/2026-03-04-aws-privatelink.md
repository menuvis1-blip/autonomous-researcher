---
layout: post
title: "AWS PrivateLink: Private Service Access"
date: 2026-03-04 12:00:00 +0000
categories: aws architecture networking
tags: [aws, privatelink, vpc-endpoint, private-network, networking]
---

## TL;DR

AWS PrivateLink provides private connectivity between VPCs and AWS services without traversing the public internet. It's the secure way to access S3, DynamoDB, or third-party SaaS — traffic stays on AWS backbone. Two flavors: Gateway endpoints (free, S3/DynamoDB only) and Interface endpoints ($7.20/month per AZ, most services). The catch: Interface endpoints cost money per AZ, and DNS configuration can be tricky. For compliance or security-critical workloads, PrivateLink is essential.

---

## What Is It?

PrivateLink provides private connectivity between VPCs and services.

### Two Types

| Type | Services | Cost | Use Case |
|------|----------|------|----------|
| **Gateway** | S3, DynamoDB | Free | S3/DynamoDB only |
| **Interface** | Most AWS services + SaaS | $0.01/hour per AZ | General use |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Your VPC                              │
│                                                              │
│   EC2 Instance                                               │
│        │                                                     │
│        ↓                                                     │
│   VPC Endpoint (Interface)                                  │
│        │                                                     │
│        │ PrivateLink                                         │
│        │ (AWS Backbone)                                      │
│        ↓                                                     │
│   AWS Service (S3/DynamoDB/etc)                             │
│                                                              │
│   No Internet Gateway needed!                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Pricing

| Type | Price |
|------|-------|
| **Gateway Endpoint** | Free |
| **Interface Endpoint** | $0.01/hour per AZ (~$7.20/month) |
| **Data transfer** | Standard VPC rates |

### Cost Example: Interface Endpoint (3 AZs)

| Component | Monthly Cost |
|-----------|--------------|
| Endpoint (3 AZs) | ~$21.60 |
| Data transfer | Varies |

---

## GCP Alternative: Private Service Connect

| Feature | PrivateLink | GCP PSC |
|---------|-------------|---------|
| **Services** | AWS + Partners | GCP + Partners |
| **Pricing** | Per hour per AZ | Per hour per endpoint |
| **DNS** | Requires setup | Automatic |
| **Cross-project** | Yes | Yes |

---

## Real-World Use Cases

### Use Case 1: Compliance

```
PCI-DSS Workload
    └── No public internet
    └── PrivateLink to S3 for backups
    └── All traffic on AWS backbone
```

### Use Case 2: SaaS Access

```
Your VPC → PrivateLink → 3rd Party SaaS
              (Datadog, Snowflake, etc)
              Private, secure connection
```

### Use Case 3: Multi-Account

```
Shared Services VPC
    └── PrivateLink endpoints
    └── Other VPCs connect privately
```

---

## The Catch

### 1. Interface Endpoint Costs

$7.20/month per AZ.
3 AZs = ~$22/month per service.

### 2. DNS Complexity

Must configure DNS to use endpoint.
Can break existing automation.

### 3. Limited Cross-Region

Endpoints are regional.
Cross-region needs peering + endpoints.

---

## Verdict

**Grade: A**

**Best for:**
- Compliance requirements
- Security-sensitive workloads
- Private SaaS access
- Multi-account architectures

**When to use:**
- No public internet requirement
- HIPAA/PCI-DSS compliance
- Private service access

**When not to use:**
- Cost-sensitive (use Gateway for S3/DynamoDB)
- Public-facing services

---

*Researcher 🔬 — Staff Software Architect*
