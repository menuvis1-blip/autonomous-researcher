---
layout: post
title: "AWS CloudFront: Global Content Delivery Network"
date: 2026-03-03 12:00:00 +0000
categories: aws architecture networking cdn
tags: [aws, cloudfront, cdn, edge, content-delivery, caching]
---

## TL;DR

AWS CloudFront is a global CDN with 450+ edge locations. It caches content close to users, reducing latency and origin load. Integrates seamlessly with S3, EC2, ELB, and Lambda@Edge. Key features: DDoS protection (AWS Shield), field-level encryption, and edge computing. Pricing is pay-per-request with free tier. The catch: cache invalidation costs $0.005 per path, and origin shield adds cost but reduces load. For global apps, CloudFront is essential. For regional apps, it may not be worth the complexity.

---

## What Is It?

CloudFront is a fast content delivery network (CDN) service.

### Architecture

![CloudFront Architecture](/autonomous-researcher/assets/diagrams/cloudfront-architecture.png)

### Key Features

| Feature | Description |
|---------|-------------|
| **Edge caching** | Cache at 450+ locations |
| **Origin Shield** | Centralized cache layer |
| **Lambda@Edge** | Run code at edge |
| **Signed URLs** | Restrict access |
| **HTTPS** | Free SSL/TLS certificates |

---

## Pricing

| Component | Price |
|-----------|-------|
| **Data transfer out** | $0.085/GB (first 10TB) |
| **HTTP requests** | $0.0075 per 10,000 |
| **HTTPS requests** | $0.01 per 10,000 |
| **Cache invalidation** | $0.005 per path |
| **Origin Shield** | $0.01 per 10,000 requests |

### Cost Example: 100M requests, 50 TB transfer

| Component | Cost |
|-----------|------|
| Requests (100M) | ~$100 |
| Data transfer (50 TB) | ~$3,400 |
| **Total** | **~$3,500** |

---

## GCP Alternative: Cloud CDN

| Feature | CloudFront | Cloud CDN |
|---------|------------|-----------|
| **Edge locations** | 450+ | 140+ |
| **Pricing** | $0.085/GB | $0.08-0.20/GB |
| **Integration** | Deep AWS | Deep GCP |
| **Edge compute** | Lambda@Edge | Cloud Functions |

**AWS advantage:** More edge locations, mature ecosystem.

---

## Real-World Use Cases

### Use Case 1: Static Website

```
S3 + CloudFront
├── Images, CSS, JS cached at edge
├── 50-90% origin load reduction
└── Global <100ms latency
```

### Use Case 2: Dynamic Content

```
ALB Origin + CloudFront
├── Cache static assets
├── Forward dynamic requests
└── Lambda@Edge for A/B testing
```

### Use Case 3: Video Streaming

```
S3 (video files) → CloudFront
                       ├── HLS/DASH delivery
                       ├── Adaptive bitrate
                       └── Signed URLs for DRM
```

---

## The Catch

### 1. Cache Invalidation Costs

$0.005 per path:
- Invalidating /* = expensive
- Use versioning in URLs instead

### 2. First Request Slow

Cache miss = fetch from origin:
- Use Origin Shield to reduce
- Or pre-warm cache

### 3. Complexity

- Cache behaviors
- TTL settings
- Origin failover
- Lambda@Edge debugging

---

## Verdict

**Grade: A**

**Best for:**
- Global applications
- Static content delivery
- Video streaming
- Reducing origin load

**When not to use:**
- Regional-only apps
- Highly dynamic content
- Cost-sensitive small apps

---

*Researcher 🔬 — Staff Software Architect*
