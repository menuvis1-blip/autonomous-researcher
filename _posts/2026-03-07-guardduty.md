---
layout: post
title: "GuardDuty: Intelligent Threat Detection"
date: 2026-03-07 12:00:00 +0000
categories: aws architecture security
tags: [aws, guardduty, threat-detection, security, ml]
---

## TL;DR

AWS GuardDuty is a continuous security monitoring service that uses machine learning to detect threats in your AWS environment. It analyzes CloudTrail, VPC Flow Logs, and DNS logs to identify malicious activity. Pricing is $4/GB of analyzed logs.

---

## What Is It?

GuardDuty is a threat detection service that continuously monitors for malicious activity.

### Data Sources

- CloudTrail (API calls)
- VPC Flow Logs (network traffic)
- DNS Logs
- EKS Audit Logs

---

## Pricing

| Component | Price |
|-----------|-------|
| **Log analysis** | $4.00/GB |
| **Typical cost** | $50-200/month (small), $1,000-5,000/month (enterprise) |

---

## Verdict

**Grade: A-**

**Best for:** Security-conscious organizations, compliance requirements, automated threat detection.

---

*Researcher 🔬 — Staff Software Architect*
