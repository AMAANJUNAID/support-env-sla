def update_sentiment(state, action):
    text = action.content.lower()

    if "sorry" in text or "apolog" in text:
        return "neutral"
    if action.action_type == "resolve":
        return "happy"
    if "wait" in text or "delay" in text:
        return "angry"

    return state["sentiment"]


def grade_step(state, action):
    reward = 0.0
    ticket = state["ticket"]

    # --- SLA DECAY ---
    state["sla_hours_left"] -= 1

    if state["sla_hours_left"] <= 0:
        reward -= 0.5

    # --- CORRECT ACTION ---
    if action.action_type == ticket["expected_action"]:
        reward += 0.5

    # --- SENTIMENT HANDLING ---
    if state["sentiment"] == "angry" and "sorry" in action.content.lower():
        reward += 0.2

    # --- ENTERPRISE STRICTNESS ---
    if ticket["customer_type"] == "enterprise":
        if action.action_type != "escalate":
            reward -= 0.3

    # --- BAD ACTIONS ---
    if action.action_type == "refund" and ticket["issue_type"] != "refund":
        reward -= 0.5

    # --- LOW QUALITY RESPONSE ---
    if len(action.content.strip()) < 5:
        reward -= 0.4

    # --- REPETITION ---
    if len(state["history"]) >= 2:
        if state["history"][-1] == state["history"][-2]:
            reward -= 0.2

    # --- DELAY PENALTY (NEW) ---
    if state["step_count"] > 3:
        reward -= 0.2

    # --- UPDATE SENTIMENT ---
    state["sentiment"] = update_sentiment(state, action)

    # --- PRIORITY MULTIPLIER ---
    if ticket["priority"] == "high":
        reward *= 1.5

    return reward


def grade_final(state):
    ticket = state["ticket"]
    history = " ".join(state["history"]).lower()

    score = 0.0

    # correct intent
    if ticket["expected_action"] in history:
        score += 0.4

    # SLA respected
    if state["sla_hours_left"] > 0:
        score += 0.3

    # sentiment improved
    if state["sentiment"] in ["neutral", "happy"]:
        score += 0.2

    # took meaningful steps
    if len(state["history"]) > 0:
        score += 0.1

    return min(score, 1.0)