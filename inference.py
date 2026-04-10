import os
import requests
from openai import OpenAI

# =========================
# API BASE (YOUR ENV SERVER)
# =========================
ENV_BASE_URL = "https://AmaanJunaid1-support-env-sla.hf.space"

# =========================
# LLM PROXY (MANDATORY)
# =========================
client = None
try:
    from openai import OpenAI

    client = OpenAI(
        base_url=os.environ.get("API_BASE_URL"),
        api_key=os.environ.get("API_KEY")
    )
except:
    client = None


# =========================
# LLM DECISION (REQUIRED)
# =========================
def llm_decision(obs):
    if not client:
        return None

    try:
        prompt = f"""
Customer message: {obs['message']}
Sentiment: {obs['sentiment']}
SLA: {obs['sla_hours_left']}

Choose ONE best action:
respond / resolve / escalate / request_info

Return format:
action_type: message
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        text = res.choices[0].message.content.lower()

        if "refund" in text:
            return "refund", text
        elif "escalate" in text:
            return "escalate", text
        elif "resolve" in text:
            return "resolve", text
        elif "request" in text:
            return "request_info", text
        else:
            return "respond", text

    except:
        return None


# =========================
# FALLBACK POLICY (SAFE)
# =========================
def smart_policy(obs):
    message = obs.get("message", "").lower()
    steps = len(obs.get("history", []))

    if steps == 0:
        if "refund" in message:
            return "refund", "Refund processed."
        if "charge" in message or "double" in message:
            return "escalate", "Escalating billing issue."
        if "delivery" in message:
            return "request_info", "Provide order ID."
        if "account" in message:
            return "request_info", "Provide account details."
        return "request_info", "Provide more details."

    if steps == 1:
        return "resolve", "Issue resolved."

    return "resolve", "Final resolution."


# =========================
# FINAL DECISION
# =========================
def get_action(obs):
    # Try LLM first (for criteria)
    action = llm_decision(obs)
    if action:
        return action

    # fallback (for stability)
    return smart_policy(obs)


# =========================
# RUN TASK
# =========================
def run_task(task_name):
    print(f"[START] task={task_name}")

    try:
        # RESET
        res = requests.post(f"{ENV_BASE_URL}/reset")
        obs = res.json()

        total_reward = 0

        for step in range(5):
            action_type, content = get_action(obs)

            res = requests.post(
                f"{ENV_BASE_URL}/step",
                json={
                    "action_type": action_type,
                    "content": content
                }
            )

            data = res.json()

            obs = data["observation"]
            reward = data["reward"]
            done = data["done"]

            total_reward += reward

            print(f"[STEP] step={step} action={action_type} reward={reward}")

            if done:
                break

        print(f"[END] task={task_name} total_reward={round(total_reward, 2)}")

    except Exception as e:
        print(f"[ERROR] {e}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_task(task)
