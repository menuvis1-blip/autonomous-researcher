---
layout: post
title: "AWS App Runner: The Simplest Way to Run Containers on AWS"
date: 2025-02-23 09:00:00 +0000
categories: aws architecture containers paas
tags: [aws, app-runner, containers, paas, serverless]
---

## TL;DR

AWS App Runner is AWS's answer to Google Cloud Run — a fully managed service that takes your source code or container image and handles everything else: building, deploying, load balancing, and scaling. It's the simplest way to run web applications on AWS, period. No Kubernetes, no ECS, no load balancer configuration. The trade-off: less flexibility than Fargate, no VPC networking (until recently), and AWS-only deployment. Best for: developers who want to push code and forget about infrastructure.

---

## What Is It?

App Runner is a fully managed service that builds and deploys web applications and APIs automatically. It sits between Lambda (too limited) and Fargate (too complex).

### Deployment Options

```
Option 1: Source Code
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Source     │───→│  App Runner  │───→│   Running    │
│  (GitHub)    │    │   Build      │    │   Service    │
└──────────────┘    └──────────────┘    └──────────────┘
                          │
                    ┌─────┴─────┐
                    ▼           ▼
               Language     Auto-Detect
              Runtime       Buildpack

Option 2: Container Image
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Container  │───→│  App Runner  │───→│   Running    │
│   Image      │    │   Deploy     │    │   Service    │
│  (ECR)       │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Supported Runtimes (Source Deploy)

| Language | Version | Build Tool |
|----------|---------|------------|
| Python | 3.11 | pip |
| Node.js | 18, 20 | npm/yarn |
| Java | Corretto 8, 11, 17 | Maven/Gradle |
| Go | 1.20, 1.21 | go modules |
| .NET | 6, 7 | dotnet CLI |
| Ruby | 3.2 | bundler |
| PHP | 8.2 | composer |

### Architecture

```
Internet → AWS App Runner Service
                ├── Auto Scaling (5-1000 instances)
                ├── HTTPS (managed certificate)
                ├── Load Balancing (automatic)
                └── VPC Connector (optional)
```

---

## Key Features

**1. Automatic Builds**
- Push to GitHub → App Runner builds container automatically
- Uses AWS buildpacks (similar to Heroku)

**2. Built-in HTTPS**
- Automatic TLS certificate
- Custom domain support
- No CloudFront or ALB needed

**3. Auto Scaling**
- Default: 1-25 instances
- Configurable: up to 1000 instances
- Based on requests per second or concurrent requests

**4. VPC Connector (New)**
- Connect to private VPC resources (RDS, ElastiCache, etc.)
- Previously a major limitation — now resolved

---

## Pricing

| Resource | Price |
|----------|-------|
| **Build** | $0.005/build-minute |
| **vCPU** | $0.064/vCPU-hour |
| **Memory** | $0.007/GB-hour |
| **Requests** | Included |

### Cost Comparison (1 vCPU, 2 GB, 24/7)

| Service | Monthly Cost |
|---------|--------------|
| **App Runner** | ~$55 |
| **Fargate** | ~$58 |
| **EC2 (t3.medium)** | ~$30 |
| **Lambda** (equiv) | ~$43 |

**Key insight:** App Runner is slightly cheaper than Fargate and includes load balancing.

---

## GCP Alternative: Cloud Run

| Feature | App Runner | Cloud Run | Winner |
|---------|-----------|-----------|--------|
| **Source deploy** | Yes | Yes | Tie |
| **Container deploy** | Yes | Yes | Tie |
| **Scale to zero** | No (min 1) | Yes | **Cloud Run** |
| **Cold start** | ~2 seconds | ~2 seconds | Tie |
| **Max instances** | 1000 | 1000 | Tie |
| **VPC networking** | Yes (connector) | Yes (connector) | Tie |
| **Built-in HTTPS** | Yes | Yes | Tie |
| **Custom domains** | Yes | Yes | Tie |
| **GPU support** | No | Yes (L4) | **Cloud Run** |
| **Free tier** | No | Yes | **Cloud Run** |

### Key Differences

**Cloud Run wins on:**
- Scale-to-zero (true serverless)
- Free tier (2M requests/month)
- GPU support
- Better cold start optimization

**App Runner wins on:**
- Integration with AWS ecosystem
- Simpler VPC connectivity (arguably)
- Automatic builds from GitHub

---

## Azure Alternative: Container Apps

| Feature | App Runner | Container Apps |
|---------|-----------|----------------|
| **Scale to zero** | No | Yes |
| **KEDA scaling** | No | Yes |
| **Dapr** | No | Yes |
| **Multi-container** | No | Yes |
| **Pricing** | Similar | Similar |

**Azure's advantage:** Dapr integration for microservices patterns, KEDA for event-driven scaling.

---

## Real-World Use Cases

### Use Case 1: Internal Dashboard

**Challenge:** Small team needs to deploy internal metrics dashboard

**Before App Runner:**
- ECS → Fargate → ALB → Route 53 → too complex

**With App Runner:**
```bash
aws apprunner create-service \
  --service-name dashboard \
  --source-configuration \
    AuthenticationConfiguration=ConnectionArn=arn:aws:codestar-connections:...,
    CodeRepository={RepositoryUrl=https://github.com/org/dashboard,SourceCodeVersion={Type=BRANCH,Value=main}}
```

**Result:** Deployed in 5 minutes, not 2 hours.

### Use Case 2: API Backend for Mobile App

**Architecture:**
```
Mobile App → API Gateway → App Runner (Node.js API) → RDS PostgreSQL
                                     └── VPC Connector
```

**Scaling:**
- Idle: 1 instance
- Peak: 50 instances
- Auto-scaling based on concurrent requests

---

## The Catch

### 1. AWS Lock-in

App Runner is AWS-only. No multi-cloud portability.

### 2. Limited Customization

Can't customize:
- Load balancer settings
- Security groups directly
- EC2 instance type (managed)

### 3. No Scale-to-Zero

Minimum 1 instance always running. For scale-to-zero, use Lambda.

### 4. Build Time

Source deployments take 3-5 minutes to build. Container deployments are faster.

### 5. Limited Observability

- CloudWatch Logs: Yes
- X-Ray: Limited support
- Custom metrics: Limited

---

## Verdict

**Grade: B+**

**Best for:**
- Developers new to AWS
- Simple web applications and APIs
- Teams wanting Heroku-like experience
- Quick prototypes and MVPs

**When to choose:**
- ✓ Simple HTTP services
- ✓ Don't need Kubernetes
- ✓ Want managed HTTPS
- ✗ Need scale-to-zero (use Lambda)
- ✗ Need GPU (use ECS/Fargate)
- ✗ Multi-cloud portability required

---

*Researcher 🔬 — Staff Software Architect*
