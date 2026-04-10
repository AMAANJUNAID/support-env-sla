def update_sentiment(state, action):
    text = action.content.lower()

    if "sorry" in text or "apolog" in text:
        return "calmer"
    if "wait" in text or "delay" in text:
        return "angry"

    return state["sentiment"]


def clamp(x):
    return max(0.01, min(x, 0.99))


# =========================
# STEP REWARD
# =========================
def grade_step(state, action):
    reward = 0.0

    state["sla_hours_left"] -= 1

    if state["sla_hours_left"] <= 0:
        return 0.01

    ticket = state["ticket"]

    if action.action_type == ticket["expected_action"]:
        reward += 0.5

    if state["sentiment"] == "angry" and "sorry" in action.content.lower():
        reward += 0.2

    if ticket["customer_type"] == "enterprise":
        if action.action_type != "escalate":
            reward -= 0.3

    if action.action_type == "refund" and ticket["issue_type"] != "refund":
        reward -= 0.5

    if len(action.content.strip()) < 5:
        reward -= 0.4

    if len(state["history"]) >= 2:
        if state["history"][-1] == state["history"][-2]:
            reward -= 0.2

    state["sentiment"] = update_sentiment(state, action)

    return clamp(reward)


# =========================
# FINAL REWARD
# =========================
def grade_final(state):
    history = " ".join(state["history"]).lower()
    ticket = state["ticket"]

    score = 0.0

    if ticket["expected_action"] in history:
        score += 0.4

    if state["sla_hours_left"] > 0:
        score += 0.3

    if state["sentiment"] != "angry":
        score += 0.2

    if len(state["history"]) > 0:
        score += 0.1

    return clamp(score)
