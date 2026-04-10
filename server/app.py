from fastapi import FastAPI, Body
from typing import Optional
from app.env import SupportEnv
from app.models import Action

app = FastAPI()

env = SupportEnv()


@app.get("/")
def root():
    return {"message": "Server running"}


# ✅ Accept BOTH empty and JSON body
@app.post("/reset")
def reset(payload: Optional[dict] = Body(default=None)):
    global env

    task_name = "easy"

    if payload and "task" in payload:
        task_name = payload["task"]

    env = SupportEnv(task_name=task_name)
    obs = env.reset()

    return obs.dict()


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)

    # 🔥 HARD SAFETY (ABSOLUTE GUARANTEE)
    if reward <= 0:
        reward = 0.01
    if reward >= 1:
        reward = 0.99

    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
