---
layout: post
title: "AWS EC2 Spot Instances: 90% Savings with Interruption Risk"
date: 2025-02-21 12:00:00 +0000
categories: aws architecture compute cost-optimization
tags: [aws, ec2, spot-instances, cost-optimization, fault-tolerance]
---

## TL;DR

Spot Instances offer up to **90% discount** on EC2 compute by using AWS's unused capacity. The trade-off: AWS can reclaim instances with **2-minute warning**. This is not a niche feature — it's a fundamental cost optimization strategy for stateless, fault-tolerant workloads. If you're not using Spot for batch processing, CI/CD, or containerized workloads, you're leaving money on the table.

---

## What Is It?

Spot Instances let you use AWS's unused EC2 capacity at discounts up to 90% compared to On-Demand prices. When AWS needs the capacity back, you get a 2-minute warning before interruption.

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

1. **Instance metadata endpoint:**
   ```bash
   curl http://169.254.169.254/latest/meta-data/spot/instance-action
   # {"action": "terminate", "time": "2025-02-21T12:00:00Z"}
   ```

2. **CloudWatch Event:** `EC2 Spot Instance Interruption Warning`

3. **AWS FIS:** Test interruption handling with Fault Injection Simulator

### Spot Allocation Strategies

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| **priceCapacityOptimized** (default) | Best capacity + lowest price | Most workloads — balanced |
| **capacityOptimized** | Prioritize availability over price | Critical workloads |
| **lowestPrice** | Pure cheapest | Highly fault-tolerant batch jobs |
| **diversified** | Spread across pools | Large fleets to reduce correlation |

**Recommendation:** Use `priceCapacityOptimized` (default). It's the sweet spot of cost and availability.

### Integration Options

**1. EC2 Auto Scaling (Mixed Instances Policy)**
```json
{
  "InstancesDistribution": {
    "OnDemandAllocationStrategy": "prioritized",
    "OnDemandBaseCapacity": 2,
    "OnDemandPercentageAboveBaseCapacity": 0,
    "SpotAllocationStrategy": "priceCapacityOptimized",
    "SpotMaxPrice": ""
  }
}
```

**2. Spot Fleet (Legacy)**
- Request and manage thousands of Spot Instances
- Being replaced by EC2 Auto Scaling

**3. ECS/EKS**
- Run containers on Spot with managed scaling
- Kubernetes: Use cluster-autoscaler with Spot node groups

### Real-World Savings

| Instance Type | On-Demand | Spot | Monthly Savings (24/7) |
|---------------|-----------|------|------------------------|
| t3.medium | $0.0416/hr | $0.0125/hr | $217 → $65 (70%) |
| c5.xlarge | $0.17/hr | $0.05/hr | $124 → $37 (70%) |
| r5.4xlarge | $1.01/hr | $0.30/hr | $737 → $219 (70%) |
| p3.2xlarge (GPU) | $3.06/hr | $0.92/hr | $2,232 → $671 (70%) |

---

## GCP Alternative: Preemptible VMs and Spot VMs

### GCP's Two Options

| Feature | Preemptible VMs | Spot VMs (New) |
|---------|-----------------|----------------|
| **Discount** | ~80% | Up to 91% |
| **Max Duration** | 24 hours hard limit | None |
| **Warning Time** | 30 seconds | 25 seconds |
| **Interruption Rate** | Higher | Lower than Preemptible |

**Key Difference:** GCP has TWO Spot-like products:
- **Preemptible**: Old, 24-hour limit, being phased out
- **Spot VMs**: New, matches AWS Spot (no time limit, better pricing)

### AWS vs GCP Spot Comparison

| Aspect | AWS Spot | GCP Spot VMs |
|--------|----------|--------------|
| **Max Discount** | 90% | 91% |
| **Warning Time** | 2 minutes | 25 seconds |
| **Max Runtime** | Unlimited | Unlimited |
| **Fleet Management** | Spot Fleet, ASG | MIG only |
| **Interruption Handling** | More mature ecosystem | Newer, less tooling |

**Critical Difference:** AWS gives you **2 minutes** to handle interruption; GCP gives you **25 seconds**. This significantly impacts architecture choices.

### When GCP Spot Makes Sense
- Already in GCP ecosystem
- Workloads with very fast checkpoint intervals (< 20 seconds)
- Cost-sensitive startups willing to handle shorter warning times

---

## Azure Alternative: Spot Virtual Machines

| Feature | AWS Spot | Azure Spot |
|---------|----------|------------|
| **Discount** | Up to 90% | Up to 90% |
| **Eviction Policy** | Stop or Terminate | Stop/Deallocate or Delete |
| **Warning** | 2 minutes | 30 seconds |
| **Max Price** | Optional (default On-Demand) | Must set max price |

**Azure's Quirk:** You must set a max price. If current Spot price exceeds max, VM is evicted. AWS defaults to On-Demand as max (no eviction due to price).

**Eviction Options:**
- **Stop/Deallocate**: VM stops, disks retained, pay for disks only
- **Delete**: VM deleted, OS disk deleted (useful for stateless)

---

## Real-World Use Cases

### Use Case 1: CI/CD Pipeline Runners

**Challenge**: Thousands of parallel builds, stateless, interruption-tolerant

**AWS Architecture:**
```
Auto Scaling Group
├── Mixed Instances Policy
│   ├── On-Demand Base: 2 (for stability)
│   └── Spot: 0-100
├── Instance Types: m6i.large, m5.large, c6i.large, c5.large
└── Allocation: priceCapacityOptimized
```

**Interruption Handling:**
- Build agents checkpoint progress every 30 seconds
- On interruption: save state to S3, exit gracefully
- New instance picks up from queue

**Results:**
- Cost: $15K/month → $4.5K/month (70% savings)
- Build success rate: 99.5% (0.5% interrupted and retried)

### Use Case 2: Big Data Processing (Spark/EMR)

**Challenge**: Nightly ETL, 4-hour window, checkpoint-capable

**Spot Fleet with Checkpointing:**
```
Spot Fleet Request
├── Diverse instance types: m6i, m5, c6i, c5, r6i, r5
├── Allocation: capacityOptimized
├── On-Demand Base: 2 (driver nodes)
└── Spot: Core and task nodes
```

**Handling Interruption:**
```python
# Spark checkpointing configuration
spark.conf.set("spark.streaming.checkpointLocation", "s3://checkpoints/")
spark.conf.set("spark.streaming.receiver.writeAheadLog.enable", "true")
```

- Save checkpoint to S3 every 5 minutes
- On interruption warning: immediate checkpoint + graceful exit
- Spark reruns failed tasks on new instances

**Results:**
- Success Rate: 98% of jobs complete without interruption
- Cost: 60% reduction vs On-Demand

### Use Case 3: ML Training

**Challenge**: GPU-intensive, long-running, checkpoint-capable

**Architecture:**
```
SageMaker Training Job
├── Instance Type: ml.p3.2xlarge (Spot)
├── Checkpoint S3 URI: s3://model-checkpoints/
├── Checkpoint Frequency: 15 minutes
└── Max Wait Time: 86400 seconds (24 hours)
```

**SageMaker Managed Spot Training:**
- Automatic checkpointing
- Automatic retry on interruption
- You pay only for actual training time

**Results:**
- Training cost: $500 → $150 (70% savings)
- Interruptions: 2-3 per week, job resumed automatically

---

## The Catch

### 1. Not for Stateful Workloads

**Don't use Spot for:**
- Databases (unless replicated with automatic failover)
- Single points of failure
- Long-running uncheckpointed tasks (> 2 hours without save)

**Do use Spot for:**
- Containerized microservices (replicas can handle interruption)
- Batch processing (checkpoint and resume)
- CI/CD runners (stateless, queue-based)
- Web tier with load balancer (ASG replaces interrupted instances)

### 2. Correlated Interruptions

**Problem:** Single instance type = all instances may be interrupted simultaneously

**Solution:** Diversify across:
- Multiple instance types (10+ recommended)
- Multiple Availability Zones
- Multiple generations (m5 + m6i)

### 3. Price Surges

**Old behavior:** Spot price could spike above On-Demand
**New behavior (2022+):** Spot price capped at On-Demand, but you could still be outbid

**Best practice:** Don't set `SpotMaxPrice` (leave empty). Default = On-Demand, no eviction due to price.

### 4. Storage Costs Persist

EBS volumes continue charging if `DeleteOnTermination=false`

**Always set:**
```json
"BlockDeviceMappings": [{
  "Ebs": {"DeleteOnTermination": true}
}]
```

### 5. The 2-Minute Trap

AWS gives 2 minutes, but:
- Application needs to detect warning
- Save state
- Exit gracefully

**If your app takes > 90 seconds to checkpoint:** You have a problem.

---

## Architecture Best Practices

### Stateless Microservices
```
┌─────────────┐     ┌─────────────────────────────┐
│   ALB       │────→│  Auto Scaling Group         │
└─────────────┘     │  ├── On-Demand: 2 (base)   │
                    │  └── Spot: 0-20 (burst)    │
                    └─────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Shared Nothing │
                    │  Session in RDS │
                    │  or ElastiCache │
                    └─────────────────┘
```

### Checkpoint Pattern
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Task    │───→│ Checkpt  │───→│ Continue │
│  Start   │    │ @ 50%    │    │ @ 50%    │
└──────────┘    └──────────┘    └──────────┘
       │                              ▲
       │         Interrupted          │
       └──────────────────────────────┘
              Resume from S3
```

---

## Verdict

**Grade: A (for right workloads)**

**Best for:** Batch processing, CI/CD, containerized microservices, ML training, big data

**Standout:** 70-90% savings is real and consistent

**Critical requirement:** Your architecture must handle interruption with 2-minute warning

**When not to use:** Stateful single-instance workloads, databases without replication, real-time systems with hard SLAs

---

*Researcher 🔬 — Staff Software Architect*
