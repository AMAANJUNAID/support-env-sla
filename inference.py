import os
from openai import OpenAI
from app.env import SupportEnv
from app.models import Action

# --- Client setup ---
client = OpenAI(
    base_url=os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

TASKS = ["easy", "medium", "hard"]


# --- Action type decision ---
def decide_action(text):
    text = text.lower()

    if "escalate" in text or "technical team" in text:
        return "escalate"
    if "refund" in text:
        return "refund"
    if "provide" in text or "details" in text or "information" in text:
        return "request_info"
    return "reply"


# --- Clean model output ---
def clean_action_text(raw_text):
    raw_text = raw_text.strip()

    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

    for line in lines:
        if len(line) > 20 and not line.lower().startswith("best next action"):
            cleaned = line[:200]
            break
    else:
        cleaned = lines[0][:200] if lines else "Sorry, I will assist you."

    # remove markdown junk
    cleaned = cleaned.replace("*", "").replace("#", "")

    return cleaned


# --- Run tasks ---
for task in TASKS:
    env = SupportEnv(task)
    obs = env.reset()

    print(f"[START] task={task} env=support_env_sla model={MODEL_NAME}")

    rewards = []
    success = False

    for step in range(1, 8):
        prompt = f"""
Customer: {obs.message}
Issue: {obs.issue_type}
Customer Type: {obs.customer_type}
Sentiment: {obs.sentiment}
SLA: {obs.sla_hours_left}

Give ONLY a short support response (1 sentence). No explanation.
"""

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )

            raw_text = response.choices[0].message.content
            action_text = clean_action_text(raw_text)

            action_type = decide_action(action_text)

            action = Action(action_type=action_type, content=action_text)

            obs, reward, done, info = env.step(action)

        except Exception as e:
            print(f"[STEP] step={step} action=error reward=0.00 done=true error={str(e)}")
            break

        rewards.append(f"{reward:.2f}")

        print(
            f"[STEP] step={step} action={action_text} reward={reward:.2f} done={str(done).lower()} error={info.get('error') or 'null'}"
        )

        if done:
            success = reward > 0.5
            break

    if rewards:
        score = sum(map(float, rewards)) / len(rewards)
    else:
        score = 0.0

    print(
        f"[END] success={str(success).lower()} steps={step} score={score:.2f} rewards={','.join(rewards)}"
    )