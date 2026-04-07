---
title: Support Env SLA
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Support Env SLA

## Overview

This project implements a realistic evaluation environment for AI agents operating in customer support workflows.

Unlike simple text-based benchmarks, this environment simulates real-world operational constraints such as:

- SLA deadlines (time pressure)
- Customer sentiment dynamics
- Enterprise vs normal customer expectations
- Multi-step decision making
- Trade-offs between speed, correctness, and cost

---

## Environment Design

Agents interact with the system using sequential actions:

- `respond`
- `resolve`
- `escalate`
- `request_info`

Each step updates:

- Customer sentiment (angry → neutral → happy)
- SLA countdown
- Conversation history

---

## Reward Function

The reward is dense and shaped across multiple dimensions:

- Correct decision making (+0.5)
- SLA compliance (+0.3)
- Sentiment improvement (+0.2)
- Enterprise penalties for wrong handling
- Escalation cost
- Delay penalties for slow resolution

This ensures agents must optimize **long-term strategy**, not just immediate responses.

---

## Task Difficulty

Three levels are provided:

### Easy
- Clear issue
- Low pressure
- Direct resolution path

### Medium
- Ambiguity in actions
- Requires reasoning
- Moderate SLA

### Hard
- High priority enterprise issue
- Strict SLA constraints
- Strong penalties for incorrect handling
- Requires escalation decisions under pressure

---

## API Endpoints

### Reset Environment