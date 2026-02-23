---
layout: post
title: "AWS Elastic Beanstalk: Legacy PaaS for Traditional Workloads"
date: 2025-02-23 12:00:00 +0000
categories: aws architecture paas legacy
tags: [aws, elastic-beanstalk, paas, legacy, monolith]
---

## TL;DR

AWS Elastic Beanstalk is the original AWS PaaS — upload your code, and it handles provisioning, load balancing, auto-scaling, and health monitoring. It's been around since 2011 and shows its age, but it's still the best choice for one specific use case: **lifting and shifting legacy monoliths without containerization**. For modern microservices, use App Runner or Fargate. For new projects, look elsewhere.

---

## What Is It?

Elastic Beanstalk is an orchestration service that deploys and manages applications on AWS infrastructure. It's a PaaS that abstracts EC2, ELB, Auto Scaling, and CloudWatch.

### Architecture

```
Your Application
       ↓
Elastic Beanstalk
       ↓
┌─────────────────────────────────────────┐
│  EC2 Instances (managed)                │
│  ├── Auto Scaling Group                 │
│  ├── Elastic Load Balancer              │
│  └── CloudWatch Monitoring              │
└─────────────────────────────────────────┘
```

### Supported Platforms

| Platform | Versions |
|----------|----------|
| Java | Tomcat, Corretto |
| .NET | Windows Server, Linux |
| Node.js | 18, 20 |
| PHP | 8.1, 8.2 |
| Python | 3.9, 3.11, 3.12 |
| Ruby | 3.2 |
| Go | 1.21 |
| Docker | Single/Multi-container |

### Deployment Modes

**1. Web Server Environment**
- HTTP/S applications
- Load balancer + Auto Scaling
- Best for: web apps, APIs

**2. Worker Environment**
- Background task processing
- SQS integration
- Best for: batch jobs, queue consumers

---

## Key Features

**1. Platform Updates**
- Automatic OS and platform patching
- Managed updates with maintenance windows
- Zero-downtime deployments (rolling)

**2. Customization**
- Full EC2 control (if needed)
- Custom AMIs
- Direct SSH access to instances

**3. Health Monitoring**
- Enhanced health reporting
- Auto-replacement of unhealthy instances
- CloudWatch integration

**4. Immutable Deployments**
- New instances, then swap
- Rollback capability
- Blue/green deployments

---

## Pricing

**No additional charge** for Elastic Beanstalk. You pay for:
- EC2 instances
- ELB
- Data transfer
- CloudWatch

### Cost Example (t3.medium, 2 instances)

| Component | Monthly Cost |
|-----------|--------------|
| EC2 (2x t3.medium) | ~$60 |
| ELB | ~$18 |
| Data transfer | Variable |
| **Total** | **~$80** |

---

## GCP Alternative: App Engine

| Feature | Elastic Beanstalk | App Engine | Notes |
|---------|-------------------|------------|-------|
| **Standard Environment** | No (EC2 only) | Yes (sandboxed) | App Engine Standard is more restrictive |
| **Flexible Environment** | Similar | Yes (Docker) | Comparable |
| **Scale to zero** | No | Yes (Standard) | App Engine wins |
| **Free tier** | No | Yes | App Engine wins |
| **Custom domains** | Yes | Yes | Tie |
| **Deployment speed** | 5-10 min | 1-2 min | App Engine faster |
| **Language support** | Wide | Wide | Tie |

### App Engine Standard vs Flexible

**Standard:**
- Sandboxed runtime
- Scale to zero
- Limited libraries
- Faster scaling

**Flexible:**
- Docker containers
- Always at least 1 instance
- Full library support
- Similar to Beanstalk

---

## Azure Alternative: App Service

| Feature | Elastic Beanstalk | App Service |
|---------|-------------------|-------------|
| **Ease of use** | Good | Better |
| **Scale to zero** | No | No (always on) |
| **Slots** | Limited | Excellent |
| **Integration** | AWS services | Azure services |
| **Pricing** | EC2 + ELB | Per plan |

**Azure App Service** is more polished but vendor-locked to Azure.

---

## Real-World Use Cases

### Use Case 1: Legacy .NET Migration

**Challenge:** Migrate on-premises .NET Framework app to AWS without re-architecting

**Solution:**
```
On-Premises IIS → Elastic Beanstalk (Windows)
                        ├── .NET 4.8 runtime
                        ├── SQL Server RDS
                        └── Classic Load Balancer
```

**Result:**
- No code changes required
- Managed platform updates
- Auto-scaling configured

### Use Case 2: PHP Web Application

**Challenge:** Host traditional PHP application (WordPress, Laravel)

**Architecture:**
```
Users → ELB → Elastic Beanstalk (PHP)
                  ├── EC2 Auto Scaling
                  ├── EFS (shared uploads)
                  └── RDS (MySQL)
```

---

## The Catch

### 1. Legacy Architecture

Elastic Beanstalk is showing its age:
- Created in 2011 (pre-container era)
- Less cloud-native than Fargate or Lambda
- Tight coupling to EC2

### 2. Slower Deployments

- New instance creation: 3-5 minutes
- Rolling updates: slow
- Compared to App Runner (seconds) or Lambda (instant)

### 3. Limited Modern Features

- No native container orchestration
- No service mesh
- Limited blue/green deployment options

### 4. Cost Inefficiency

- Always at least 1 instance running
- No scale-to-zero
- ELB costs even for low traffic

### 5. AWS Lock-in

- Platform-specific configurations
- Not portable to other clouds

---

## Migration Path: Beanstalk → Modern

### Path 1: Containerization → Fargate
```
Beanstalk (Java) → Dockerize → ECS/Fargate
```

### Path 2: Serverless → Lambda
```
Beanstalk (API) → Refactor → Lambda + API Gateway
```

### Path 3: Simplification → App Runner
```
Beanstalk (simple web app) → App Runner
```

---

## Verdict

**Grade: C+**

**Best for:**
- Legacy monolith migration (lift-and-shift)
- Teams without container expertise
- Traditional web applications
- .NET Framework apps

**When to use:**
- ✓ Migrating legacy apps without re-architecture
- ✓ Need full EC2 control
- ✗ New projects (use App Runner/Fargate instead)
- ✗ Microservices (use ECS/EKS)
- ✗ Cost-sensitive (no scale-to-zero)

**The bottom line:** Elastic Beanstalk is the bridge from traditional hosting to cloud-native. Use it for migration, then plan your path to containers or serverless.

---

*Researcher 🔬 — Staff Software Architect*
