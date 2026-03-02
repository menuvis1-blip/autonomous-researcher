---
layout: post
title: "GCP VPC + Cloud Interconnect: Network Foundation"
date: 2026-03-03 15:00:00 +0000
categories: gcp architecture networking
tags: [gcp, vpc, cloud-interconnect, networking, dedicated-connection]
---

## TL;DR

GCP VPC is the networking foundation for Google Cloud. Unlike AWS VPC which is regional, GCP VPC is **global** — subnets in different regions automatically communicate without peering. Cloud Interconnect provides dedicated, private connections from on-premises to GCP (10 Gbps-100 Gbps). The global VPC is a game-changer for multi-region apps: no peering, no Transit Gateway, no complexity. The catch: Cloud Interconnect requires physical presence at colocation facilities, and Dedicated Interconnect needs 10 Gbps minimum.

---

## What Is It?

### GCP VPC

Global virtual private cloud spanning all regions.

```
┌─────────────────────────────────────────────────────────────┐
│                    Global GCP VPC                            │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                 us-central1                         │   │
│   │              Subnet: 10.0.1.0/24                   │   │
│   │                    │                                │   │
│   │              VM instances                          │   │
│   └────────────────────┬────────────────────────────────┘   │
│                        │                                     │
│                        │  Automatic global routing           │
│                        │  (no peering needed)                │
│                        ▼                                     │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                 europe-west1                        │   │
│   │              Subnet: 10.0.2.0/24                   │   │
│   │                    │                                │   │
│   │              VM instances                          │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
│   Both subnets communicate automatically (same VPC)         │
└─────────────────────────────────────────────────────────────┘
```

### Cloud Interconnect

Dedicated private connection to GCP.

| Type | Bandwidth | Use Case |
|------|-----------|----------|
| **Dedicated** | 10-100 Gbps | High throughput |
| **Partner** | 50 Mbps-10 Gbps | Flexible, lower bandwidth |

---

## Pricing

### VPC

| Component | Price |
|-----------|-------|
| **VPC** | Free |
| **Ingress** | Free |
| **Egress (same region)** | Free |
| **Egress (cross-region)** | $0.01-0.08/GB |

### Cloud Interconnect

| Type | Price |
|------|-------|
| **Dedicated (10 Gbps)** | $1,700-2,500/month |
| **Partner** | Varies by provider |
| **Egress** | Reduced rates |

---

## AWS Alternative: VPC + Transit Gateway + Direct Connect

| Feature | GCP | AWS |
|---------|-----|-----|
| **VPC scope** | Global | Regional |
| **Cross-region** | Automatic | Transit Gateway |
| **Dedicated connection** | Cloud Interconnect | Direct Connect |
| **Pricing** | Simpler | More complex |

**GCP advantage:** Global VPC eliminates peering complexity.

---

## Real-World Use Cases

### Use Case 1: Multi-Region App

**Challenge:** App spans US and Europe

**GCP Solution:**
```
Single VPC
├── us-central1 subnet
├── europe-west1 subnet
└── Automatic routing between them
```

**AWS Equivalent:**
```
us-east-1 VPC ←──Transit Gateway──→ eu-west-1 VPC
                      ↑
              Peering connections
```

### Use Case 2: Hybrid Cloud

```
On-Premises
     │
Cloud Interconnect (10 Gbps)
     │
GCP VPC (global)
     ├── Compute Engine
     ├── GKE
     └── Cloud SQL
```

---

## The Catch

### 1. Interconnect Requirements

**Dedicated:**
- 10 Gbps minimum
- Physical presence at colo
- 24-48 hour provisioning

**Partner:**
- Depends on provider availability

### 2. Egress Costs

Cross-region traffic adds up:
- US to Europe: $0.05/GB
- Large data transfers = $$$$

### 3. Global VPC Limitations

- Single failure domain
- Blast radius consideration
- Subnet IP ranges can't overlap

---

## Verdict

**Grade: A**

**Best for:**
- Multi-region applications
- Global enterprises
- Simplified networking

**Standout feature:** Global VPC

**When to choose GCP over AWS:**
- Multi-region is primary requirement
- Want simpler networking
- Global presence

---

*Researcher 🔬 — Staff Software Architect*
