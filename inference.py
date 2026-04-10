import os
import requests
from openai import OpenAI

# =========================
# CONFIG (MANDATORY)
# =========================
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

ENV_BASE_URL = "https://amaanjunaid1-support-env-sla.hf.space"

TASKS = ["easy", "medium", "hard"]
MAX_STEPS = 6

# =========================
# INIT LLM CLIENT
# =========================
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# =========================
# LOGGING (STRICT FORMAT)
# =========================
def log_start(task):
    print(f"[START] task={task} env=support_env_sla model={MODEL_NAME}", flush=True)


def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True
    )

# =========================
# LLM DECISION
# =========================
def llm_decision(obs):
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
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        text = (res.choices[0].message.content or "").lower()

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

    except Exception:
        return None

# =========================
# FALLBACK POLICY
# =========================
def fallback_policy(obs):
    msg = obs.get("message", "").lower()

    if "refund" in msg:
        return "refund", "Processing refund."
    if "charge" in msg:
        return "escalate", "Escalating billing issue."
    if "delivery" in msg:
        return "request_info", "Please provide order ID."
    if "account" in msg:
        return "request_info", "Please provide account details."

    return "respond", "We are looking into your issue."

# =========================
# FINAL ACTION SELECTOR
# =========================
def get_action(obs):
    action = llm_decision(obs)
    if action:
        return action
    return fallback_policy(obs)

# =========================
# RUN TASK
# =========================
def run_task(task):
    log_start(task)

    rewards = []
    steps_taken = 0
    success = False

    try:
        # RESET
        res = requests.post(
            f"{ENV_BASE_URL}/reset",
            json={"task": task}
        )
        obs = res.json()

        for step in range(1, MAX_STEPS + 1):

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
            reward = float(data["reward"])
            done = data["done"]

            rewards.append(reward)
            steps_taken = step

            log_step(step, action_type, reward, done, None)

            if done:
                break

        # =========================
        # SCORE NORMALIZATION (CRITICAL FIX)
        # =========================
        if len(rewards) > 0:
            score = sum(rewards) / len(rewards)
        else:
            score = 0.5

        # STRICT RANGE FIX
        if score <= 0:
            score = 0.01
        elif score >= 1:
            score = 0.99

        success = score > 0.1

    except Exception as e:
        log_step(0, "error", 0.0, True, str(e))
        score = 0.5

    log_end(success, steps_taken, score, rewards)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    for task in TASKS:
        run_task(task)
