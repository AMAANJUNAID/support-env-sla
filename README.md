# 🚀 Support Env SLA  
### Where AI stops answering… and starts making decisions

---

## 🧠 The Reality

Most AI models look impressive until they face real-world constraints.

In customer support:
- Users are impatient 😡  
- Deadlines matter ⏱️  
- Wrong decisions cost money 💸  
- Conversations are multi-step 🔁  

👉 And suddenly, “smart AI” starts failing.

---

## 💡 What I Built

**Support Env SLA** — a simulation environment to evaluate AI agents under **real operational pressure**.

This isn’t about generating responses.

It’s about:
> Making the right decision at the right time under constraints.

---

## ⚙️ What Makes This Different

Unlike typical AI benchmarks, this environment introduces:

### ⏱️ Time Pressure (SLA)
Agents must act before deadlines expire — delay = penalty

---

### 😡 Dynamic Customer Sentiment
Actions directly affect mood:
```text
angry → neutral → happy
```
---
## 🏢 Real Customer Types

Enterprise customers:

- stricter expectations
- higher penalties
- require escalation strategies

---
## 🔁 Multi-Step Decision Making

One step isn’t enough.
Agents must:

- plan
- adapt
- recover from mistakes

---

## ⚖️ Trade-Offs (The Hard Part)

Agents must balance:

- Speed vs Accuracy
- Cost vs Satisfaction
- Resolution vs Escalation

👉 There is no “always correct” answer

---

## 🎯 Available Actions
```
respond        → communicate  
resolve        → fix issue  
escalate       → send to higher support  
request_info   → gather details  
```

---

🧪 Task Difficulty
```
Level                      What Happens
🟢 Easy	                   Clear issue, low pressure
🟡 Medium	               Ambiguity, reasoning needed
🔴 Hard	                   Enterprise + strict SLA + high penalties
```

---


## 📊 Reward System (What Actually Matters)

The environment evaluates:

- ✔️ Correct decisions
- ⏳ SLA compliance
- 😡 Sentiment handling
- ⚠️ Mistakes & delays
- 🔁 Efficiency across steps

👉 This forces long-term reasoning, not shortcuts.

---
🧪 Run Locally
```
pip install -r requirements.txt
python inference.py
```
---
🧠 Why This Matters

Most AI evaluation today is:
```
 Single-step → Static → Unrealistic
```
This project moves toward:
```
 Multi-step → Dynamic → Real-world aligned
```
👉 This is how AI should be evaluated.

## 🛠️ Tech Stack
- FastAPI
- Python
- OpenAI API
- Docker
- Hugging Face Spaces



