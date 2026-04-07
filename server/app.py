from fastapi import FastAPI
from app.env import SupportEnv
from app.models import Action

app = FastAPI()

# global env instance
env = SupportEnv()


@app.get("/")
def root():
    return {"message": "Server running"}


# ✅ MUST accept task from inference.py
@app.post("/reset")
def reset(payload: dict):
    global env

    task_name = payload.get("task", "easy")

    env = SupportEnv(task_name=task_name)

    obs = env.reset()

    return obs.dict()


# ✅ STEP endpoint
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)

    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }


# ✅ REQUIRED FOR OPENENV VALIDATION
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


# ✅ REQUIRED ENTRYPOINT
if __name__ == "__main__":
    main()