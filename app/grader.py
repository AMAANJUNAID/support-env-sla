def update_sentiment(state, action):
    text = action.content.lower()

    if "sorry" in text or "apolog" in text:
        return "calmer"
    if "wait" in text or "delay" in text:
        return "angry"

    return state["sentiment"]


# =========================
# STEP REWARD (SMALL ONLY)
# =========================
def grade_step(state, action):
    reward = 0.2  # keep small to avoid overflow

    state["sla_hours_left"] -= 1

    if state["sla_hours_left"] <= 0:
        return 0.05

    ticket = state["ticket"]

    if action.action_type == ticket["expected_action"]:
        reward += 0.2

    if state["sentiment"] == "angry" and "sorry" in action.content.lower():
        reward += 0.1

    state["sentiment"] = update_sentiment(state, action)

    return float(reward)


# =========================
# FINAL REWARD
# =========================
def grade_final(state):
    history = " ".join(state["history"]).lower()
    ticket = state["ticket"]

    score = 0.3

    if ticket["expected_action"] in history:
        score += 0.3

    if state["sla_hours_left"] > 0:
        score += 0.2

    if state["sentiment"] != "angry":
        score += 0.1

    return float(score)
