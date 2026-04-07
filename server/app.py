from fastapi import FastAPI
from app.env import SupportEnv
from app.models import Action

app = FastAPI()

env = SupportEnv()

@app.get("/")
def root():
    return {"message": "Server running"}

@app.post("/reset")
def reset():
    return env.reset().dict()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }