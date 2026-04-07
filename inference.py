import os
import requests
from openai import OpenAI

# =========================
# REQUIRED ENV VARIABLES
# =========================
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# optional (for docker image use)
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# =========================
# OPENAI CLIENT (MANDATORY)
# =========================
client = OpenAI(api_key=HF_TOKEN)

TASKS = ["easy", "medium", "hard"]


def choose_action(obs):
    """
    Simple baseline policy using LLM (required usage)
    """

    prompt = f"""
    You are a customer support agent.

    Ticket: {obs['message']}
    Sentiment: {obs['sentiment']}
    SLA hours left: {obs['sla_hours_left']}
    Issue type: {obs['issue_type']}
    Customer type: {obs['customer_type']}

    Choose ONE action from:
    - respond
    - resolve
    - escalate
    - request_info

    Return only the action type.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        action_type = response.choices[0].message.content.strip().lower()

        # safety fallback
        if action_type not in ["respond", "resolve", "escalate", "request_info"]:
            action_type = "respond"

    except Exception:
        # fallback if API fails
        action_type = "respond"

    return {
        "action_type": action_type,
        "content": "We are handling your request."
    }


def run_task(task_name):
    print(f"[START] task={task_name}")

    total_reward = 0.0

    # reset env
    res = requests.post(f"{API_BASE_URL}/reset", json={"task": task_name})
    obs = res.json()

    done = False
    step = 0

    while not done:
        step += 1

        action = choose_action(obs)

        res = requests.post(f"{API_BASE_URL}/step", json=action)
        data = res.json()

        obs = data["observation"]
        reward = data["reward"]
        done = data["done"]

        total_reward += reward

        # REQUIRED LOG FORMAT
        print(f"[STEP] step={step} action={action['action_type']} reward={reward}")

        if step > 10:
            break

    print(f"[END] task={task_name} total_reward={round(total_reward, 2)}\n")

    return total_reward


def main():
    scores = []

    for task in TASKS:
        score = run_task(task)
        scores.append(score)

    final_score = sum(scores) / len(scores)

    print(f"[FINAL SCORE] {round(final_score, 3)}")


if __name__ == "__main__":
    main()