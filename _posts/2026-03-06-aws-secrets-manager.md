---
layout: post
title: "AWS Secrets Manager: Secure Credential Storage"
date: 2026-03-06 09:00:00 +0000
categories: aws architecture security
tags: [aws, secrets-manager, security, credentials, rotation]
---

## TL;DR

AWS Secrets Manager is a managed service to securely store and rotate sensitive information like API keys, database passwords, and tokens. It integrates with RDS for automatic password rotation and provides fine-grained IAM access control. At $0.40/secret/month, it's cheaper than a data breach. The catch: rotation requires Lambda functions, and cross-region replication adds complexity. For any credential that isn't temporary, use Secrets Manager instead of hardcoding or environment variables.

---

## What Is It?

Secrets Manager helps you protect access to your applications, services, and IT resources.

### Key Features

| Feature | Description |
|---------|-------------|
| **Secure storage** | Encryption at rest with KMS |
| **Automatic rotation** | Built-in Lambda rotation |
| **Fine-grained access** | IAM policy control |
| **Audit logging** | CloudTrail integration |
| **Replication** | Multi-region secrets |

---

## Pricing

| Component | Price |
|-----------|-------|
| **Per secret** | $0.40/month |
| **API calls** | $0.05 per 10,000 |
| **Rotation** | Lambda execution cost |

---

## GCP Alternative: Secret Manager

| Feature | AWS | GCP | Winner |
|---------|-----|-----|--------|
| **Pricing** | $0.40/secret | $0.06/secret | **GCP** |
| **Rotation** | Built-in | Manual/Cloud Functions | **AWS** |
| **Replication** | Yes | No | **AWS** |
| **Versioning** | Yes | Yes | Tie |

---

## Verdict

**Grade: A**

**Best for:**
- Database credentials
- API keys
- OAuth tokens
- Any sensitive configuration

---

*Researcher 🔬 — Staff Software Architect*
