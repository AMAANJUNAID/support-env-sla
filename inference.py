import requests
import time

BASE_URL = "http://localhost:7860"  # change automatically if needed

TASKS = ["easy", "medium", "hard"]


def run_task(task_name):
    print(f"[START] task={task_name}")

    total_reward = 0.0

    # reset
    res = requests.post(f"{BASE_URL}/reset", json={"task": task_name})
    obs = res.json()

    done = False
    step = 0

    while not done:
        step += 1

        # --- SIMPLE POLICY (baseline) ---
        if obs["sentiment"] == "angry":
            action_type = "respond"
            content = "Sorry for the inconvenience, we are working on it."
        elif obs["sla_hours_left"] <= 1:
            action_type = "escalate"
            content = "Escalating this issue immediately."
        else:
            action_type = "resolve"
            content = "Your issue has been resolved."

        action = {
            "action_type": action_type,
            "content": content
        }

        res = requests.post(f"{BASE_URL}/step", json=action)
        data = res.json()

        obs = data["observation"]
        reward = data["reward"]
        done = data["done"]

        total_reward += reward

        print(f"[STEP] {step} action={action_type} reward={reward}")

        if step > 10:
            break

    print(f"[END] task={task_name} total_reward={round(total_reward,2)}\n")

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