---
layout: post
title: "GCP Workflows + Eventarc: Orchestration and Events"
date: 2026-03-09 15:00:00 +0000
categories: gcp architecture integration
tags: [gcp, workflows, eventarc, orchestration, events]
---

## TL;DR

GCP Workflows orchestrates multiple Google Cloud services into serverless workflows. Eventarc provides event ingestion for triggering workflows. Together they provide event-driven orchestration. Pricing is $0.025/million steps for Workflows and $0/million for Eventarc (preview). The catch: Workflows lacks visual design (YAML only), and Eventarc has limited sources compared to EventBridge.

---

## What Is It?

### Workflows
Orchestrates Google Cloud services in serverless workflows.

### Eventarc
Routes events from Google Cloud sources to Cloud Run, Workflows, etc.

---

## Pricing

| Component | Price |
|-----------|-------|
| **Workflows** | $0.025 per million steps |
| **Eventarc** | Free (during preview) |

---

## AWS Comparison

| Feature | Workflows/Eventarc | Step Functions/EventBridge | Winner |
|---------|-------------------|---------------------------|--------|
| **Visual design** | No | Yes | AWS |
| **Event sources** | GCP only | 200+ AWS + SaaS | AWS |
| **Pricing** | Per step | Per transition | Similar |
| **Complexity** | Simpler | More features | GCP |

---

## Verdict

**Grade: B+**

**Best for:**
- GCP-native orchestration
- Simple workflows
- Cloud Run integration

---

*Researcher 🔬 — Staff Software Architect*
