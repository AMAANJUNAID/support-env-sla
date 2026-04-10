import os
import requests
from openai import OpenAI

# =========================
# API BASE (YOUR ENV SERVER)
# =========================
ENV_BASE_URL = "https://AmaanJunaid1-support-env-sla.hf.space"


def run_task(task):
    print(f"[START] task={task}")

    obs = requests.post(f"{BASE_URL}/reset", json={"task": task}).json()

    done = False
    total_reward = 0

    step = 0

    while not done:
        action = {
            "action_type": "request_info",
            "content": "Please provide more details"
        }

        res = requests.post(f"{BASE_URL}/step", json=action).json()

        reward = res["reward"]
        done = res["done"]

        print(f"[STEP] step={step} reward={reward}")

        # 🔥 CRITICAL FIX
        if done:
            total_reward = reward

        step += 1

    print(f"[END] task={task} total_reward={total_reward}\n")


if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run_task(t)
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
