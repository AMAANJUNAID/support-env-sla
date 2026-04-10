def update_sentiment(state, action):
    text = action.content.lower()

    if "sorry" in text or "apolog" in text:
        return "calmer"
    if "wait" in text or "delay" in text:
        return "angry"

    return state["sentiment"]


# =========================
# STEP REWARD
# =========================
def grade_step(state, action):
    reward = 0.0

    # SLA decay
    state["sla_hours_left"] -= 1

    # ❌ DO NOT RETURN NEGATIVE / ZERO
    if state["sla_hours_left"] <= 0:
        return 0.01

    ticket = state["ticket"]

    # ✅ correct action
    if action.action_type == ticket["expected_action"]:
        reward += 0.5

    # ✅ sentiment handling
    if state["sentiment"] == "angry" and "sorry" in action.content.lower():
        reward += 0.2

    # ❌ enterprise strictness
    if ticket["customer_type"] == "enterprise":
        if action.action_type != "escalate":
            reward -= 0.3

    # ❌ refund misuse
    if action.action_type == "refund" and ticket["issue_type"] != "refund":
        reward -= 0.5

    # ✅ apology bonus
    if action.action_type == "reply" and "sorry" in action.content.lower():
        reward += 0.3

    # ❌ useless answer
    if len(action.content.strip()) < 5:
        reward -= 0.4

    # ❌ repetition penalty
    if len(state["history"]) >= 2:
        if state["history"][-1] == state["history"][-2]:
            reward -= 0.2

    # update sentiment
    state["sentiment"] = update_sentiment(state, action)

    # 🔥 FINAL CLAMP (STRICT RANGE)
    reward = max(0.01, min(reward, 0.99))

    return round(reward, 2)


# =========================
# FINAL REWARD
# =========================
def grade_final(state):
    history = " ".join(state["history"]).lower()
    ticket = state["ticket"]

    score = 0.0

    # ✅ correct intent achieved
    if ticket["expected_action"] in history:
        score += 0.4

    # ✅ SLA respected
    if state["sla_hours_left"] > 0:
        score += 0.3

    # ✅ sentiment improved
    if state["sentiment"] != "angry":
        score += 0.2

    # ✅ valid interaction
    if len(state["history"]) > 0:
        score += 0.1

    # 🔥 STRICT RANGE FIX
    score = max(0.01, min(score, 0.99))

    return round(score, 2)
