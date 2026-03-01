---
layout: post
title: "AWS Transit Gateway: Centralized VPC Hub"
date: 2026-03-02 12:00:00 +0000
categories: aws architecture networking
tags: [aws, transit-gateway, vpc, networking, hub-and-spoke]
---

## TL;DR

AWS Transit Gateway is the hub-and-spoke solution for connecting multiple VPCs and on-premises networks. Instead of managing hundreds of VPC peering connections, you connect everything to Transit Gateway once. It scales to thousands of VPCs and supports VPN/Direct Connect for hybrid cloud. The catch: $36/month per attachment + data transfer costs. For 3-5 VPCs, peering is cheaper. For 10+ VPCs, Transit Gateway pays for itself in reduced complexity.

---

## What Is It?

Transit Gateway is a network transit hub that interconnects VPCs and on-premises networks.

### Architecture

```
                          ┌─────────────────┐
                          │  On-Premises    │
                          │  Data Center    │
                          └────────┬────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
              ┌─────▼─────┐  ┌────▼────┐  ┌─────▼─────┐
              │Direct     │  │   VPN   │  │   VPN     │
              │Connect    │  │Tunnel   │  │  Backup   │
              └─────┬─────┘  └────┬────┘  └─────┬─────┘
                    │             │              │
                    └─────────────┼──────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │      Transit Gateway       │
                    │         (Hub)              │
                    └─────────────┬──────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            │         │           │           │         │
      ┌─────▼───┐ ┌───▼────┐ ┌────▼───┐ ┌─────▼───┐ ┌──▼────┐
      │  VPC 1  │ │ VPC 2  │ │ VPC 3  │ │ VPC 4   │ │ VPC 5 │
      │Production│ │  Dev   │ │Staging │ │ Shared  │ │ DMZ   │
      └─────────┘ └────────┘ └────────┘ └─────────┘ └───────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Hub-and-spoke** | Central connectivity |
| **Route tables** | Segment traffic |
| **Multicast** | One-to-many communication |
| **Peering** | Inter-region Transit Gateway |

---

## Pricing

| Component | Price |
|-----------|-------|
| **Transit Gateway** | Free (attachment-based) |
| **VPC Attachment** | $0.05/hour (~$36/month) |
| **VPN Attachment** | $0.05/hour (~$36/month) |
| **Data processing** | $0.02/GB |

**Cost for 10 VPCs:** 10 × $36 = $360/month base

---

## GCP Alternative: Cloud Router + VPC Peering

| Feature | Transit Gateway | GCP Cloud Router |
|---------|-----------------|------------------|
| **Hub-and-spoke** | Native | VPC Peering mesh |
| **Scalability** | 5000+ attachments | Limited by peering |
| **Price** | Per attachment | Per peering |

**AWS advantage:** Purpose-built hub-and-spoke.

---

## Real-World Use Cases

### Use Case 1: Enterprise Multi-VPC

**Challenge:** 50 VPCs across 3 regions

**Solution:**
```
Regional Transit Gateways → Peered → Central TGW
        ↓
   Route tables by department
   (Prod, Dev, Shared, Security)
```

### Use Case 2: Hybrid Cloud

```
Transit Gateway
├── VPC attachments (20 VPCs)
├── Direct Connect (primary)
└── VPN (backup)
```

---

## The Catch

### 1. Cost at Scale

20 VPCs = $720/month just for attachments.

### 2. Single Point of Failure

If TGW fails, all connectivity fails.
- Use multiple TGWs in critical environments
- Multi-AZ redundancy built-in

### 3. Route Table Complexity

Hundreds of routes = management challenge.
- Use automation (Terraform)
- Segment with multiple route tables

---

## Verdict

**Grade: A**

**Best for:**
- 10+ VPCs
- Hybrid cloud connectivity
- Network segmentation

**When to use:**
- VPC count > 10
- Need centralized control
- Multi-region connectivity

**When not to use:**
- 2-5 VPCs (peering is cheaper)
- Simple setups

---

*Researcher 🔬 — Staff Software Architect*
