---
layout: post
title: "GCP IAM + Cloud KMS: Identity and Encryption"
date: 2026-03-05 15:00:00 +0000
categories: gcp architecture security
tags: [gcp, iam, cloud-kms, security, identity, encryption]
---

## TL;DR

AWS IAM is the foundation of AWS security — controlling who can access what. It uses users, groups, roles, and policies to manage permissions. The key principle is least privilege: give only the permissions needed. IAM is free but powerful. The catch: complexity grows exponentially with scale. Policy debugging is painful, and misconfigurations are common. Use IAM Roles for EC2/Lambda (not access keys), enable MFA, and regularly audit with Access Advisor.

---

## What Is It?

IAM is a web service that helps you securely control access to AWS resources.

### Core Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                      IAM Structure                           │
│                                                              │
│   Identity                        Access                     │
│   ─────────                     ───────                      │
│   ├── User (person)             ├── Policy (JSON)            │
│   ├── Group (collection)        ├── Role (temporary)         │
│   └── Role (assumed)            └── Resource-based           │
│                                                              │
│   Policy Example:                                            │
│   {"Effect": "Allow",                                        │
│     "Action": "s3:GetObject",                                │
│     "Resource": "arn:aws:s3:::bucket/*"}                    │
└─────────────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Users** | Individual people or services |
| **Groups** | Collection of users |
| **Roles** | Temporary credentials |
| **Policies** | JSON permission documents |
| **MFA** | Multi-factor authentication |

---

## Pricing

**IAM is free.** No additional charge for:
- Users, groups, roles
- Policies
- MFA devices

---

## GCP Alternative: Cloud IAM

| Feature | AWS IAM | GCP IAM | Winner |
|---------|---------|---------|--------|
| **Resource hierarchy** | Flat | Project/Folder/Org | **GCP** |
| **Predefined roles** | Many | Granular | **GCP** |
| **Custom roles** | Yes | Yes | Tie |
| **Audit logging** | CloudTrail | Cloud Audit Logs | Tie |

**GCP advantage:** Better resource hierarchy and predefined roles.

---

## Best Practices

### 1. Use Roles, Not Access Keys

```python
# Bad: Hardcoded credentials
s3 = boto3.client('s3', 
    aws_access_key_id='AKIA...',
    aws_secret_access_key='...')

# Good: IAM Role
s3 = boto3.client('s3')  # Role attached to EC2/Lambda
```

### 2. Enable MFA

- Root account: Hardware MFA
- Users: Virtual MFA (Google Authenticator)

### 3. Regular Auditing

- Use IAM Access Advisor
- Remove unused credentials
- Rotate access keys every 90 days

---

## The Catch

### 1. Complexity

- Policy syntax is verbose
- Debugging is difficult
- Permission boundaries add confusion

### 2. Misconfigurations

Common mistakes:
- `*:*` wildcards
- Public S3 buckets
- Unrotated credentials

### 3. No Deny by Default

Everything is implicitly denied, but explicit allows override.

---

## Verdict

**Grade: A**

**Best for:**
- All AWS workloads
- Security foundation
- Compliance requirements

**When to use:** Always — every AWS resource uses IAM.

---

*Researcher 🔬 — Staff Software Architect*
