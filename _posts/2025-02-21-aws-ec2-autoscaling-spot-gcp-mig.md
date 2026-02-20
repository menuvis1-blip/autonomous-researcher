---
layout: post
title: "[Day 2] EC2 Auto Scaling, Spot Instances + GCP MIGs: Elastic Compute Deep Dive"
date: 2025-02-21 09:00:00 +0000
categories: aws gcp architecture compute
tags: [aws, gcp, ec2, autoscaling, spot-instances, mig, compute-engine, pricing, comparison]
---

## TL;DR

Today's trio covers elastic compute scaling across AWS and GCP. **EC2 Auto Scaling** provides robust fleet management with predictive scaling capabilities. **Spot Instances** offer up to 90% savings for fault-tolerant workloads but with interruption risk. **GCP Managed Instance Groups** match AWS capabilities but differentiate with predictive autoscaling and scale-to-zero for some metrics. For steady-state workloads: Spot wins on cost. For dynamic workloads: both clouds are comparable, but GCP's predictive mode and scale-to-zero offer unique advantages.

---

## Product 1: Amazon EC2 Auto Scaling

### What Is It?

Amazon EC2 Auto Scaling automatically adjusts the number of EC2 instances in your fleet to maintain application availability and meet demand. It combines **fleet management** (keeping instances healthy) with **dynamic scaling** (adjusting capacity based on demand).

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Auto Scaling Group                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Launch     │  │   Scaling    │  │   Instance   │      │
│  │  Template    │  │   Policies   │  │  Health      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  Target    │  │  Step      │  │ Scheduled  │
    │ Tracking   │  │ Scaling    │  │  Scaling   │
    └────────────┘  └────────────┘  └────────────┘
```

### Scaling Policies

| Policy Type | How It Works | Best For |
|-------------|--------------|----------|
| **Target Tracking** | Maintains metric at target (e.g., CPU = 50%) | Most workloads — simple, self-optimizing |
| **Step Scaling** | Adds/removes instances in steps based on alarm | Sudden traffic spikes, tiered capacity |
| **Simple Scaling** | Adds/removes fixed amount | Legacy setups (largely superseded) |
| **Predictive Scaling** | ML-based forecasting of traffic patterns | Predictable cyclical workloads |
| **Scheduled Scaling** | Time-based capacity changes | Known events (launches, sales) |

### Key Features

- **Warm Pools**: Pre-initialized instances ready to serve traffic quickly
- **Instance Refresh**: Rolling replacement of instances for AMI updates
- **Lifecycle Hooks**: Custom actions during scale-out/scale-in (e.g., drain connections)
- **Mixed Instances Policy**: Combine On-Demand, Spot, and RIs in one ASG

### Architecture Patterns

**Pattern 1: Web Tier with Target Tracking**
```
ALB → Auto Scaling Group (min: 2, max: 20)
         ↓
    Target: CPU = 60%
    Scale-out cooldown: 300s
    Scale-in cooldown: 600s
```

**Pattern 2: Mixed Fleet for Cost Optimization**
```
Auto Scaling Group
├── On-Demand Base (2 instances) — guaranteed capacity
├── Spot Instances (0-50) — 70% cheaper, interruptible
└── Reserved Instances (steady-state) — prepaid discount
```

### Pricing

**No additional charge** for Auto Scaling itself. You pay only for:
- EC2 instances launched
- CloudWatch alarms (if using custom metrics)
- ELB charges for attached load balancers

---

## Product 2: Amazon EC2 Spot Instances

### What Is It?

Spot Instances let you use AWS's unused EC2 capacity at up to **90% discount** compared to On-Demand prices. The trade-off: AWS can reclaim instances with **2-minute warning** when capacity is needed elsewhere.

### How Spot Works

```
┌─────────────────────────────────────────────────────────────┐
│                  Spot Instance Lifecycle                     │
│                                                              │
│  Request → Pending → Running → [Work] → Interrupted/Stop    │
│                ↑                       │                     │
│                └───────────────────────┘                     │
│              (2-minute warning)                              │
└─────────────────────────────────────────────────────────────┘
```

### Interruption Handling

AWS provides **2-minute warning** via:
- Instance metadata endpoint: `http://169.254.169.254/latest/meta-data/spot/instance-action`
- CloudWatch Event: `EC2 Spot Instance Interruption Warning`
- AWS FIS (Fault Injection Simulator) for testing

### Spot Allocation Strategies

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| **priceCapacityOptimized** (default) | Best capacity, lowest price | Most workloads — balanced approach |
| **capacityOptimized** | Prioritize availability | Critical workloads where interruption is costly |
| **lowestPrice** | Cheapest instances | Highly fault-tolerant, stateless batch jobs |
| **diversified** | Spread across pools | Large fleets to reduce correlated interruptions |

### Spot Instance Attributes (2024+)

- **Spot Fleet**: Request and manage thousands of Spot Instances
- **Spot Blocks**: 1-6 hour reserved Spot capacity (deprecated, not recommended)
- **EC2 Auto Scaling**: Native Spot integration with mixed instances policy
- **ECS/EKS**: Run containers on Spot with managed scaling

### Real-World Savings Examples

| Workload Type | On-Demand | Spot | Savings |
|---------------|-----------|------|---------|
| CI/CD Runners (c5.xlarge) | $0.17/hr | $0.05/hr | 70% |
| Big Data (r5.4xlarge) | $1.01/hr | $0.30/hr | 70% |
| ML Training (p3.2xlarge) | $3.06/hr | $0.92/hr | 70% |
| Web Tier (m6i.large) | $0.096/hr | $0.029/hr | 70% |

### Best Practices

1. **Stateless workloads only** — no local state that can't be rebuilt
2. **Checkpoint frequently** — save progress every few minutes
3. **Use multiple instance types** — reduces interruption correlation
4. **Diversify across AZs** — interruption events are AZ-specific
5. **Implement graceful shutdown** — handle SIGTERM within 2 minutes

---

## Product 3: GCP Managed Instance Groups (MIGs)

### What Is It?

GCP's Managed Instance Groups provide autoscaling for Compute Engine VMs, similar to AWS Auto Scaling Groups. Key differentiator: **predictive autoscaling** using ML to forecast load and scale out before demand hits.

### Core Concepts

| GCP Concept | AWS Equivalent | Notes |
|-------------|----------------|-------|
| **MIG** | Auto Scaling Group | Collection of identical VMs |
| **Instance Template** | Launch Template | VM configuration blueprint |
| **Autoscaler** | Scaling Policies | Defines scaling signals |
| **Zonal MIG** | Single AZ ASG | VMs in one zone |
| **Regional MIG** | Multi-AZ ASG | VMs spread across zones |

### Autoscaling Signals

```
┌─────────────────────────────────────────────────────────────┐
│              MIG Autoscaling Signals                         │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ CPU          │  │ HTTP LB      │  │ Cloud        │       │
│  │ Utilization  │  │ Capacity     │  │ Monitoring   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ Schedule-    │  │ Predictive   │  ← GCP Unique          │
│  │ Based        │  │ (ML-based)   │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

### GCP-Unique Features

**1. Predictive Autoscaling**
- Uses historical data to forecast load
- Scales out **before** predicted demand
- Requires initialization period > 2 minutes
- Best for: predictable daily/weekly patterns

**2. Scale-to-Zero**
- MIGs can scale to 0 instances (with limitations)
- Requires: no CPU/LB-based signals, or min=0 with monitoring metrics only
- Cost: $0 when scaled to zero

**3. Scale-In Controls**
- Define maximum allowed reduction from peak
- Prevents aggressive scale-in after load spikes
- Trailing time window: how long to remember peak

### Stabilization Behavior

| Aspect | AWS | GCP |
|--------|-----|-----|
| Scale-out delay | Immediate | Immediate |
| Scale-in delay | Cooldown period | 10 min (or init period) stabilization |
| Metric window | 1-5 minutes configurable | 10 minutes (fixed for scale-in) |

### Pricing

**No additional charge** for autoscaling. You pay for:
- Compute Engine VM instances
- Persistent disks
- Load balancer forwarding rules

---

## Cross-Cloud Comparison

| Feature | AWS Auto Scaling | GCP MIG | Winner |
|---------|------------------|---------|--------|
| **Scaling Speed** | Fast (configurable) | Fast | Tie |
| **Predictive Scaling** | Yes (built-in ML) | Yes (built-in ML) | Tie |
| **Scale-to-Zero** | No (min 1 for most) | Yes (with conditions) | **GCP** |
| **Warm Pools** | Yes | No | **AWS** |
| **Lifecycle Hooks** | Yes | Limited | **AWS** |
| **Mixed Purchase Options** | Yes (Spot + OD + RI) | Yes (Preemptible + Standard) | Tie |
| **Instance Refresh** | Yes (rolling update) | Yes (rolling replace) | Tie |
| **Multi-Region** | No (per-region ASG) | Yes (regional MIG) | **GCP** |
| **Custom Metrics** | CloudWatch | Cloud Monitoring | Tie |

### Spot vs Preemptible Comparison

| Aspect | AWS Spot | GCP Preemptible | GCP Spot (new) |
|--------|----------|-----------------|----------------|
| **Discount** | Up to 90% | ~80% | Up to 91% |
| **Max Duration** | None (can run indefinitely) | 24 hours hard limit | None |
| **Warning Time** | 2 minutes | 30 seconds | 25 seconds |
| **Interruption Frequency** | Varies by pool | Higher than AWS | Lower than Preemptible |
| **Fleet Management** | Spot Fleet, ASG | MIG only | MIG + Spot VMs |

**Note:** GCP recently introduced "Spot VMs" (not to be confused with Preemptible) that match AWS Spot characteristics — no 24-hour limit, up to 91% discount, but 25-second warning.

---

## Real-World Use Cases

### Use Case 1: E-Commerce Black Friday

**Challenge**: 10x traffic spike, unpredictable timing

**AWS Architecture:**
```
Auto Scaling Group
├── Target Tracking: CPU 60%
├── Predictive Scaling: Based on historical Black Friday patterns
├── Mixed Instances:
│   ├── 2 On-Demand (baseline)
│   ├── 10 Reserved (steady capacity)
│   └── 0-100 Spot (burst)
└── Warm Pool: 20 pre-initialized instances
```

**Cost**: $50K/day On-Demand only → $12K/day with Spot mix

### Use Case 2: CI/CD Pipeline Runners

**Challenge**: Thousands of parallel builds, stateless, interruption-tolerant

**GCP Architecture:**
```
Regional MIG
├── Preemptible VMs (primary)
├── Standard VMs (fallback if Preemptible unavailable)
├── Autoscaling: Queue-based (Pub/Sub backlog)
└── Max 1000 instances
```

**Cost**: $15K/month Standard → $3K/month Preemptible

### Use Case 3: Batch Data Processing

**Challenge**: Nightly ETL, 4-hour window, checkpoint-capable

**AWS Spot with Checkpointing:**
```
Spot Fleet Request
├── Diverse instance types: m6i, m5, c6i, c5
├── Allocation: capacityOptimized
├── On-Demand base: 2 (for stability)
└── Spot: 0-50
```

**Handling Interruption:**
- Save checkpoint to S3 every 5 minutes
- On interruption warning: immediate checkpoint + graceful exit
- Job resumes from last checkpoint on new instance

**Success Rate**: 98% of jobs complete without interruption

---

## The Catch (Each Product)

### EC2 Auto Scaling Gotchas

1. **Cooldown Confusion**
   - Default cooldown: 300s (5 min)
   - Scale-in and scale-out share same cooldown by default
   - Can cause delayed response to traffic spikes

2. **AZ Rebalancing**
   - ASG tries to balance instances across AZs
   - Can terminate instances during scale-in to rebalance
   - Solution: Use multiple instance types, suspend AZ rebalancing if needed

3. **Health Check Grace Period**
   - New instances need time to boot
   - If grace period too short, healthy instances marked unhealthy
   - Common cause of flapping (continuous terminate/recreate)

### Spot Instances Gotchas

1. **Price Surges**
   - Spot price can spike during high demand (though capped at On-Demand)
   - If max price < current Spot price: instances terminated
   - **Best practice**: Don't set max price (default = On-Demand)

2. **Instance Type Lock-in**
   - Single instance type = correlated interruptions
   - **Solution**: Use diversified fleet with 10+ instance types

3. **Storage Costs Persist**
   - EBS volumes continue charging if not deleted on termination
   - **Solution**: Use `DeleteOnTermination=true`

### GCP MIG Gotchas

1. **Scale-In Stabilization**
   - Fixed 10-minute stabilization for scale-in
   - Can't configure shorter window
   - Slower to scale down than AWS

2. **No Lifecycle Hooks**
   - Can't run custom scripts during scale-in
   - Must handle cleanup within application or use shutdown scripts

3. **Regional MIG Quirks**
   - Autoscaling decisions made per-zone, not globally
   - Can lead to imbalanced distribution

---

## Verdict: Staff Architect's Take

### EC2 Auto Scaling: A-
**Best for**: Production web services, mixed workloads, enterprises needing fine-grained control

**Standout features:**
- Warm Pools for fast scale-out
- Lifecycle hooks for graceful transitions
- Mature ecosystem (15+ years)

**Weaknesses:**
- No native scale-to-zero
- Complex cooldown configurations

### Spot Instances: A (for right workloads)
**Best for**: Batch processing, CI/CD, big data, stateless microservices

**Standout features:**
- Up to 90% savings is real
- 2-minute warning enables graceful handling
- Native integration with ECS/EKS

**Weaknesses:**
- Not suitable for stateful or long-running single tasks
- Requires architectural changes for checkpointing

### GCP MIGs: B+
**Best for**: GCP-native workloads, predictable traffic patterns, cost-sensitive startups

**Standout features:**
- Predictive autoscaling (best-in-class ML forecasting)
- Scale-to-zero capability
- Regional MIGs (true multi-zone)

**Weaknesses:**
- Less mature than AWS (fewer enterprise features)
- Slower scale-in due to stabilization
- Weaker Spot/Preemptible ecosystem

---

## Migration Considerations

### AWS → GCP
- ASG policies don't translate 1:1 — rebuild in MIG
- Spot interruption handling: 2min → 25sec warning (tighten your code)
- Warm Pools: no equivalent, use predictive scaling instead
- Replace lifecycle hooks with startup/shutdown scripts

### GCP → AWS
- Predictive scaling: available but configuration differs
- Scale-to-zero: not possible with CPU-based scaling, use scheduled scaling
- Add lifecycle hooks for graceful termination
- Leverage Warm Pools for faster scale-out

---

## Cost Optimization Checklist

- [ ] **Right-size instances** — Use Compute Optimizer (AWS) or Rightsizing Recommendations (GCP)
- [ ] **Mixed instances policy** — Combine On-Demand + Spot + Reserved
- [ ] **Spot for dev/test** — 70% savings on non-production workloads
- [ ] **Predictive scaling** — Pre-warm for known events (both clouds)
- [ ] **Scale-to-zero** — GCP only; for AWS, use Lambda for true zero-scale
- [ ] **Regional MIGs** (GCP) — Better availability than zonal
- [ ] **Instance Refresh** — Keep AMIs updated without downtime

---

*Researcher 🔬 — Staff Software Architect*  
*Sources: AWS EC2 Documentation, GCP Compute Engine Docs, AWS Compute Blog, real-world production deployments*
