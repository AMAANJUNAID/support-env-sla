def update_sentiment(state, action):
    text = action.content.lower()

    if "sorry" in text or "apolog" in text:
        return "calmer"
    if "wait" in text or "delay" in text:
        return "angry"
    return state["sentiment"]


def grade_step(state, action):
    reward = 0.0

    # SLA decay
    state["sla_hours_left"] -= 1
    if state["sla_hours_left"] <= 0:
        return -1.0

    ticket = state["ticket"]

    # correct decision
    if action.action_type == ticket["expected_action"]:
        reward += 0.5

    # sentiment handling
    if state["sentiment"] == "angry" and "sorry" in action.content.lower():
        reward += 0.2

    # enterprise customers are stricter
    if ticket["customer_type"] == "enterprise":
        if action.action_type != "escalate":
            reward -= 0.3

    # refund misuse penalty
    if action.action_type == "refund" and ticket["issue_type"] != "refund":
        reward -= 0.5
    if action.action_type == "reply" and "sorry" in action.content.lower():
        reward += 0.3
    # useless answer
    if len(action.content.strip()) < 5:
        reward -= 0.4

    # repetition penalty
    if len(state["history"]) >= 2:
        if state["history"][-1] == state["history"][-2]:
            reward -= 0.2

    state["sentiment"] = update_sentiment(state, action)

    return reward


def grade_final(state):
    history = " ".join(state["history"]).lower()
    ticket = state["ticket"]

    score = 0.0

    # correct intent achieved
    if ticket["expected_action"] in history:
        score += 0.4

    # SLA respected
    if state["sla_hours_left"] > 0:
        score += 0.3

    # sentiment improved
    if state["sentiment"] != "angry":
        score += 0.2

    # no random actions
    if len(state["history"]) > 0:
        score += 0.1

    return min(score, 1.0)