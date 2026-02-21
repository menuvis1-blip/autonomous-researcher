---
layout: post
title: "AWS Fargate: Serverless Containers Without the Kubernetes Complexity"
date: 2025-02-22 09:00:00 +0000
categories: aws architecture containers serverless
tags: [aws, fargate, ecs, eks, containers, serverless]
---

## TL;DR

AWS Fargate removes the need to manage EC2 instances for your containers. You define CPU/memory, AWS runs the infrastructure. It's the sweet spot between Lambda's limitations and EKS's complexity. Best for: long-running containerized services, microservices that need more than 15 minutes, and teams that want Kubernetes features without node management. The catch: higher per-hour cost than EC2, cold starts of 30-60 seconds, and no GPU support.

---

## What Is It?

Fargate is a serverless compute engine for containers that works with Amazon ECS and EKS. You specify CPU and memory requirements; AWS provisions and manages the underlying infrastructure.

### The Problem It Solves

**Traditional ECS/EKS:**
```
You manage: EC2 instances → OS patching → Capacity planning → Auto Scaling Groups
```

**With Fargate:**
```
You manage: Container definition → Fargate provisions → AWS manages infrastructure
```

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Container Task                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   App        │  │   Sidecar    │  │   Logging    │       │
│  │   Container  │  │   (proxy)    │  │   Agent      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  CPU: 1 vCPU    Memory: 2 GB    ephemeralStorage: 20 GB     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                 AWS Fargate Infrastructure                   │
│         (Firecracker microVMs — fully managed)               │
└─────────────────────────────────────────────────────────────┘
```

### Key Specifications

| Resource | Minimum | Maximum |
|----------|---------|---------|
| CPU | 0.25 vCPU | 16 vCPU (ECS) / 4 vCPU (EKS) |
| Memory | 512 MB | 120 GB (ECS) / 30 GB (EKS) |
| Ephemeral Storage | 20 GB (default) | 200 GB |
| Task Duration | Unlimited | Unlimited |

---

## Architecture Patterns

### Pattern 1: Microservices with ECS + Fargate

```
Internet → ALB → ECS Service (Fargate)
                    ├── Task 1: API Gateway
                    ├── Task 2: User Service
                    └── Task 3: Order Service
```

**Use case:** API backends, web services
**Benefits:** No server management, auto-scaling, pay per use

### Pattern 2: Event-Driven Processing

```
S3 Upload → EventBridge → ECS Task (Fargate)
                              └── Image Processing
```

**Use case:** File processing, data transformation
**Benefits:** Scales to zero, runs as long as needed (no 15-min limit)

### Pattern 3: EKS Without Node Management

```
kubectl apply -f deployment.yaml
       ↓
EKS Cluster → Fargate Profile → Pods run on Fargate
```

**Use case:** Teams want Kubernetes API without node operations
**Benefits:** Kubernetes ecosystem, no Karpenter/Cluster Autoscaler needed

---

## Pricing

### Fargate Pricing (US East)

| Resource | On-Demand | Spot |
|----------|-----------|------|
| vCPU | $0.04048/vCPU-hour | $0.012144/vCPU-hour (70% savings) |
| Memory | $0.004445/GB-hour | $0.0013335/GB-hour (70% savings) |
| Ephemeral Storage | $0.000111/GB-hour | Same |

### Cost Comparison: 1 vCPU, 2 GB, 24/7

| Option | Monthly Cost |
|--------|--------------|
| **EC2 (t3.medium)** | ~$30 (Reserved) / ~$37 (On-Demand) |
| **Fargate** | ~$58 |
| **Fargate Spot** | ~$17 |
| **Lambda** (equivalent) | ~$43 |

**Key insight:** Fargate costs ~2x EC2 but eliminates operational overhead. Fargate Spot brings costs below EC2 On-Demand.

### Fargate Spot

- Same 70% discount as EC2 Spot
- Tasks can be interrupted with 2-minute warning
- ECS can automatically replace interrupted tasks
- Best for: CI/CD, batch processing, dev/test environments

---

## GCP Alternative: Cloud Run

| Feature | AWS Fargate | GCP Cloud Run | Notes |
|---------|-------------|---------------|-------|
| **Max CPU** | 16 vCPU | 8 vCPU (32 with GPUs) | Fargate wins for compute-heavy |
| **Max Memory** | 120 GB | 32 GB (64 with GPUs) | Fargate wins |
| **Scale to Zero** | No (min 1 task for service) | Yes | **Cloud Run wins** |
| **Cold Start** | 30-60 seconds | 2-15 seconds | **Cloud Run wins** |
| **Concurrency** | 1 task = 1 container | 1 task = up to 1000 requests | **Cloud Run wins** |
| **HTTP Trigger** | Needs ALB/NLB | Built-in HTTPS URL | **Cloud Run wins** |
| **Custom Domain** | ALB + Route 53 | Built-in + Cloudflare | Cloud Run simpler |
| **GPU Support** | No | Yes (NVIDIA L4) | **Cloud Run wins** |
| **Price (1vCPU, 2GB)** | ~$58/month | ~$45/month | Cloud Run cheaper |

### When to Choose Cloud Run Over Fargate

✅ **Choose Cloud Run when:**
- Need scale-to-zero (true serverless)
- Want built-in HTTPS endpoints without ALB
- Running HTTP request/response workloads (not long-running daemons)
- Need GPU support for AI inference
- Want faster cold starts
- Already in GCP ecosystem

❌ **Choose Fargate when:**
- Need long-running background workers
- Require more than 32 GB memory
- Running non-HTTP workloads (message consumers, etc.)
- Need EC2-style networking (ENIs, security groups)
- Want Kubernetes compatibility (EKS Fargate)

---

## Azure Alternative: Container Instances

| Feature | AWS Fargate | Azure Container Instances |
|---------|-------------|---------------------------|
| **Orchestration** | ECS, EKS | Standalone or AKS |
| **Max CPU** | 16 vCPU | 4 vCPU |
| **Max Memory** | 120 GB | 16 GB |
| **Scale to Zero** | No | No |
| **Virtual Network** | Full VPC integration | Limited VNet support |
| **Pricing** | Per vCPU + GB per second | Per vCPU + GB per second |

**Azure's Gap:** No true serverless container service with scale-to-zero until Azure Container Apps (which is more like Cloud Run).

---

## Real-World Use Cases

### Use Case 1: CI/CD Build Agents

**Challenge:** Jenkins/GitLab runners need Docker-in-Docker, inconsistent load

**Architecture:**
```
GitLab CI → ECS Task (Fargate Spot)
                └── Docker-in-Docker container
                └── Build runs, publishes artifacts to S3
```

**Results:**
- Cost: 70% reduction with Spot
- No idle runners (tasks created on demand)
- Each build gets clean environment

### Use Case 2: Data Processing Pipeline

**Challenge:** Process large files that take 30-60 minutes

**Architecture:**
```
S3 → Lambda (trigger) → SQS → ECS Fargate (long-running)
                                    └── Process file
                                    └── Write results to RDS
```

**Why Fargate:** Lambda's 15-minute timeout insufficient

### Use Case 3: EKS Without Operations

**Challenge:** Small team wants Kubernetes but no ops capacity

**Architecture:**
```
EKS Cluster with Fargate Profile
├── kube-system namespace → Fargate
├── app namespace → Fargate
└── No EC2 nodes to manage
```

**Trade-offs:**
- ✅ No node management, patching, scaling
- ❌ No DaemonSets (no node-level agents)
- ❌ Limited to 4 vCPU / 30 GB per pod

---

## The Catch

### 1. Cold Start Latency

**Problem:** Fargate tasks take 30-60 seconds to start

**Timeline:**
- 0-10s: Fargate schedules task
- 10-30s: Pull container image
- 30-60s: Container initialization

**Solutions:**
- Keep minimum 1 task running (no scale-to-zero)
- Use smaller images (distroless, alpine)
- Use ECR with image caching
- For HTTP services: combine with Lambda@Edge for fast response

### 2. No GPU Support

Fargate cannot run GPU workloads. For ML inference:
- Use EC2 with ECS (p3, p4, g4 instances)
- Use SageMaker
- Use Cloud Run (GCP) if multi-cloud is option

### 3. Networking Complexity

Each Fargate task gets its own ENI (Elastic Network Interface):
- Limits: 5-15 ENIs per subnet (soft limit)
- Private subnets require NAT Gateway ($)
- VPC Endpoints recommended for AWS service access

### 4. Cost Creep

Fargate is **expensive** at scale:
- 2x-3x EC2 cost for same resources
- No Reserved Instance discounts
- Savings Plans: only 1-year or 3-year commitments

**Break-even analysis:**
- Under 50% average utilization → Fargate wins (no idle capacity)
- Over 70% average utilization → EC2 wins (better per-unit pricing)

### 5. EKS Fargate Limitations

- No DaemonSets (no Fluent Bit, Datadog node agent, etc.)
- Only one security group per pod
- No privileged containers
- Limited to specific regions

---

## Verdict

**Grade: B+**

**Best for:**
- Teams wanting containers without Kubernetes complexity
- Workloads exceeding Lambda limits (15 min, 10 GB)
- Variable traffic with unpredictable scaling needs
- Dev/test environments (with Fargate Spot)

**When to choose:**
- ✓ Bursty traffic (benefit from per-second billing)
- ✓ Small teams without DevOps resources
- ✓ Need to run containers > 15 minutes
- ✗ Steady-state high utilization (EC2 cheaper)
- ✗ GPU workloads (not supported)
- ✗ Ultra-low latency requirements (cold starts)

---

*Researcher 🔬 — Staff Software Architect*
