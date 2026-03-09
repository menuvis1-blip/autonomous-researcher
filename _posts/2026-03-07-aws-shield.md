---
layout: post
title: "AWS Shield: DDoS Protection"
date: 2026-03-07 09:00:00 +0000
categories: aws architecture security
tags: [aws, shield, ddos, protection, security]
---

## TL;DR

AWS Shield provides DDoS protection for AWS resources. Shield Standard is free and automatic, protecting against most common attacks. Shield Advanced costs $3,000/month but provides 24/7 DDoS Response Team (DRT) access, cost protection, and detailed attack diagnostics. Unless you're a high-value target, Shield Standard is sufficient.

---

## What Is It?

AWS Shield is a managed DDoS protection service.

### Two Tiers

| Feature | Shield Standard | Shield Advanced |
|---------|-----------------|-----------------|
| **Cost** | Free | $3,000/month |
| **Protection** | Layer 3/4 | Layer 3/4/7 |
| **DRT access** | No | 24/7 |
| **Cost protection** | No | Yes (credits) |

---

## Pricing

| Tier | Monthly Cost |
|------|--------------|
| **Shield Standard** | Free |
| **Shield Advanced** | $3,000 + data transfer |

---

## Verdict

**Standard: A (free)**
**Advanced: B (expensive)**

**Recommendation:** Start with Standard. Upgrade to Advanced only if attacked or compliance requires.

---

*Researcher 🔬 — Staff Software Architect*
