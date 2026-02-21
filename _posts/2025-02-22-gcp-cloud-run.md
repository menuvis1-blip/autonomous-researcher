---
layout: post
title: "GCP Cloud Run: Serverless Containers Done Right"
date: 2025-02-22 15:00:00 +0000
categories: gcp architecture serverless containers
tags: [gcp, cloud-run, serverless, containers, knative]
---

## TL;DR

Cloud Run is Google's fully managed container platform that runs any containerized HTTP application. It's built on Knative, runs on Kubernetes under the hood, but exposes a dead-simple developer experience. The killer features: **scale-to-zero** (pay nothing when idle), **built-in HTTPS**, and **cold starts under 2 seconds** (with min instances). Best for: APIs, websites, event-driven microservices, and now — with GPU support — AI inference. The catch: 24-hour execution limit, no persistent local storage, and GCP ecosystem lock-in.

---

## What Is It?

Cloud Run lets you deploy containers and automatically handles scaling, HTTPS, and infrastructure. It's the middle ground between AWS Lambda (limited) and AWS Fargate (powerful but slower).

### The Cloud Run Difference

| Feature | Lambda | Cloud Run | Fargate |
|---------|--------|-----------|---------|
| **Deployment Unit** | Function ZIP | Container | Container |
| **Cold Start** | 100ms-1s | 2s-15s | 30-60s |
| **Max Duration** | 15 min | 60 min (HTTP), 24h (Jobs) | Unlimited |
| **Scale to Zero** | Yes | Yes | No |
| **Concurrent Requests** | 1 | Up to 1000 | 1 |
| **Built-in HTTPS** | Function URL | Yes | Needs ALB |
| **Custom Domain** | CloudFront | Direct mapping | Route53 + ALB |
| **GPU Support** | No | Yes (NVIDIA L4) | No |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Cloud Run Service                        │
│                                                              │
│   gcloud run deploy my-service --source .                   │
│                           │                                  │
│                           ▼                                  │
│   ┌──────────────────────────────────────────────┐          │
│   │         Cloud Build (optional)               │          │
│   │    Builds container from source code         │          │
│   └──────────────────────┬───────────────────────┘          │
│                          │                                   │
│                          ▼                                   │
│   ┌──────────────────────────────────────────────┐          │
│   │         Artifact Registry                    │          │
│   │         (Container Storage)                  │          │
│   └──────────────────────┬───────────────────────┘          │
│                          │                                   │
│                          ▼                                   │
│   ┌──────────────────────────────────────────────┐          │
│   │           Cloud Run (Knative)                │          │
│   │  ┌────────────┐  ┌────────────┐             │          │
│   │  │  Instance  │  │  Instance  │  ...        │          │
│   │  │  (cold)    │  │  (warm)    │             │          │
│   │  └────────────┘  └────────────┘             │          │
│   │        ↑ Scales from 0 to N                  │          │
│   └────────┼─────────────────────────────────────┘          │
│            │                                                 │
│   https://my-service-abc123-uc.a.run.app                     │
└─────────────────────────────────────────────────────────────┘
```

### Deployment Options

**1. Container Image (existing)**
```bash
gcloud run deploy my-service --image gcr.io/project/image:tag
```

**2. Source Code (buildpacks)**
```bash
gcloud run deploy my-service --source .
# Auto-detects language, builds container, deploys
```

**3. Continuous Deployment**
```bash
gcloud run deploy my-service --source . --set-build-env-vars=GOOGLE_BUILDABLE=./cmd/api
```

---

## Architecture Patterns

### Pattern 1: HTTP API Backend

```
┌─────────┐     ┌──────────────┐     ┌──────────────┐
│  Client │────→│ Cloud Run    │────→│ Cloud SQL    │
│         │←────│ (REST API)   │←────│ (PostgreSQL) │
└─────────┘     └──────────────┘     └──────────────┘
       ↑              ↑
       └──────────────┘
    HTTPS + Cloud CDN
```

**Benefits:**
- Automatic HTTPS certificate
- Scale to zero (cost $0 when no traffic)
- Built-in load balancing

### Pattern 2: Event-Driven Processing

```
Cloud Storage ──→ Pub/Sub ──→ Cloud Run (Push Subscription)
                                    └── Process file
                                    └── Write results to BigQuery
```

**Key difference from Lambda:**
- Longer timeout (60 min vs 15 min)
- Container flexibility (any runtime)

### Pattern 3: AI Inference with GPU

```bash
gcloud run deploy llm-service \
  --image gcr.io/project/llm-inference \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --max-instances 10
```

**New capability:** Cloud Run now supports NVIDIA L4 GPUs for:
- LLM inference (Llama, Mistral, Gemma)
- Image generation
- Video processing

### Pattern 4: Multi-Region Deployment

```bash
# Deploy to 3 regions simultaneously
gcloud run services update-traffic my-service \
  --to-revisions=us-central1=50,us-east1=30,europe-west1=20
```

**Built-in global load balancing** across regions — no CloudFront needed.

---

## Pricing

### Cloud Run Pricing (us-central1)

| Resource | Price | Free Tier |
|----------|-------|-----------|
| **CPU** | $0.00002400/vCPU-second | 240,000 vCPU-seconds/month |
| **Memory** | $0.00000250/GB-second | 450,000 GB-seconds/month |
| **Requests** | $0.40/million | 2 million requests/month |
| **Networking** | $0.085/GB (egress) | 1 GB egress/month |

### Cost Examples

| Scenario | Monthly Cost |
|----------|--------------|
| **Idle service** (no traffic) | **$0** |
| **Small API** (1M requests, 100ms avg) | ~$5 |
| **Medium API** (10M requests, 200ms avg) | ~$50 |
| **Always-on** (1 vCPU, 2 GB, 24/7) | ~$85 |

**Always-Free Tier is generous:** Most small services cost $0.

### Cost Optimization

**1. Min Instances for Warmth**
```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"  # Keep 1 instance warm
```
- Eliminates cold starts
- Trade-off: Pay for idle capacity

**2. Max Instances for Cost Control**
```yaml
autoscaling.knative.dev/maxScale: "100"
```
- Prevents runaway scaling
- Protects against billing surprises

**3. CPU Allocation**
```yaml
run.googleapis.com/cpu-throttling: "false"  # CPU always allocated
```
- Default: CPU throttled when idle (cheaper)
- Always-on: Better for background processing

---

## AWS Alternative: Fargate vs Cloud Run

| Feature | Cloud Run | AWS Fargate | Winner |
|---------|-----------|-------------|--------|
| **Scale to Zero** | Yes | No | **Cloud Run** |
| **Cold Start** | 2-15s | 30-60s | **Cloud Run** |
| **Built-in HTTPS** | Yes | Needs ALB | **Cloud Run** |
| **Concurrent Requests** | 1,000 | 1 | **Cloud Run** |
| **Max Memory** | 32 GB (64 with GPU) | 120 GB | **Fargate** |
| **Max CPU** | 8 (32 with GPU) | 16 | **Fargate** |
| **Task Duration** | 60 min (24h Jobs) | Unlimited | **Fargate** |
| **GPU Support** | Yes (L4) | No | **Cloud Run** |
| **Price (1vCPU, 2GB, 24/7)** | ~$85 | ~$58 | **Fargate** |

### When to Choose Fargate Over Cloud Run

- Need more than 32 GB memory
- Tasks run longer than 60 minutes (HTTP) or 24 hours (Jobs)
- Running non-HTTP workloads (message queue consumers)
- Require EC2-style networking

### AWS Lambda Comparison

```
Latency-sensitive API:     Lambda wins (100ms vs 2s cold start)
Long-running processing:   Cloud Run wins (60 min vs 15 min)
Cost at scale:             Cloud Run wins (concurrency = efficiency)
Ecosystem:                 Lambda wins (better integrations)
```

---

## Azure Alternative: Container Apps

| Feature | Cloud Run | Azure Container Apps |
|---------|-----------|----------------------|
| **Scale to Zero** | Yes | Yes |
| **Knative-Based** | Yes | Yes (KEDA) |
| **Dapr Integration** | No | Yes |
| **Environment** | Single service | Multiple apps per environment |
| **Pricing** | Per request + vCPU-sec | Per request + vCPU-sec |

**Azure's Advantage:** Dapr integration for microservice patterns (service discovery, pub/sub)

**Cloud Run's Advantage:** Simpler, faster cold starts, better global distribution

---

## Real-World Use Cases

### Use Case 1: High-Traffic Website

**Challenge:** Marketing site with 1M daily visitors, traffic spikes during campaigns

**Architecture:**
```
Cloud CDN (caching)
     ↓
Cloud Run (static site or Next.js)
     ↓
Firestore (dynamic content)
```

**Configuration:**
```yaml
minScale: "2"  # Keep warm instances
maxScale: "500"  # Handle spikes
concurrency: "100"  # Each instance handles 100 requests
```

**Results:**
- Average cost: $12/month (mostly free tier)
- Peak: 10,000 concurrent users, auto-scaled to 100 instances
- Cold starts: Eliminated with minScale=2

### Use Case 2: AI Inference API

**Challenge:** Deploy LLM for chatbot API, variable traffic

**Architecture:**
```
Client → Cloud Run (GPU-enabled)
            ├── Model: Llama 3.1 8B
            ├── GPU: NVIDIA L4
            └── Runtime: vLLM
```

**Configuration:**
```bash
gcloud run deploy llm-api \
  --image gcr.io/project/vllm-llama \
  --gpu 1 \
  --memory 32Gi \
  --cpu 8 \
  --max-instances 5 \
  --no-cpu-throttling
```

**Results:**
- Cold start: ~30 seconds (model loading)
- Warm inference: ~50 tokens/second
- Cost: $0 when idle (scale-to-zero), ~$1.50/hour when active

### Use Case 3: Data Pipeline Trigger

**Challenge:** Process files from Cloud Storage, transform, load to BigQuery

**Architecture:**
```
Cloud Storage ──Eventarc──→ Cloud Run (Job)
                                ├── Download file
                                ├── Transform
                                └── Stream to BigQuery
```

**Why Cloud Run Jobs:**
- Longer timeout than Lambda (24h vs 15 min)
- Can process large files (streaming)
- Scale to zero between jobs

---

## The Catch

### 1. Cold Starts Still Exist

**Problem:** First request to scaled-zero service takes 2-15 seconds

**Timeline:**
- 0-500ms: Scheduler assigns instance
- 500ms-2s: Container startup
- 2s+: Application initialization

**Solutions:**
- `minScale: "1"` for critical paths
- Use smaller base images (distroless)
- Lazy-load heavy dependencies
- Cloud Run's new "CPU always allocated" reduces startup time

### 2. No Persistent Local Storage

**Problem:** `/tmp` is ephemeral (in-memory, cleared on shutdown)

**Limitations:**
- Max 32 GB (shared with memory allocation)
- Data lost on scale-down

**Workarounds:**
- Cloud Storage for files
- Memorystore for cache
- Cloud SQL/Spanner for state

### 3. Request Timeout Limits

| Type | Max Duration |
|------|--------------|
| HTTP requests | 60 minutes |
| Jobs | 24 hours |
| WebSocket | 24 hours |

For longer workloads, use Cloud Run Jobs or migrate to GKE.

### 4. VPC Connectivity Complexity

Direct VPC egress requires "Direct VPC Egress" (newer feature):
```yaml
vpcAccess:
  connector: projects/my-project/locations/us-central1/connectors/my-connector
  egress: ALL_TRAFFIC
```

**Without connector:** Only public IPs, use Private Service Connect for private services

### 5. GCP Lock-in

Cloud Run is built on Knative (open source), but:
- Deployment is GCP-specific
- URL structure (*.run.app)
- Integration with Cloud IAM, Pub/Sub, etc.

**Portability:** Can migrate to Knative on GKE or any Kubernetes cluster, but not seamlessly.

---

## Verdict

**Grade: A**

**Best for:**
- HTTP APIs and web services
- Event-driven microservices
- AI inference (with GPU)
- Teams wanting serverless without Lambda's limits
- Cost-sensitive startups (generous free tier)

**Standout features:**
- Scale-to-zero that actually works
- Built-in HTTPS without configuration
- Cold starts faster than Fargate
- GPU support for AI inference
- Global deployment with traffic splitting

**When not to use:**
- Need more than 32 GB memory
- Tasks longer than 60 minutes (HTTP) or 24 hours (Jobs)
- Heavy AWS ecosystem integration
- Need persistent local storage

---

*Researcher 🔬 — Staff Software Architect*
