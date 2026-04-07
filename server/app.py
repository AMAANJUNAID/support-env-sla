from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server running"}

# 👉 THIS IS REQUIRED
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

# 👉 THIS IS ALSO REQUIRED
if __name__ == "__main__":
    main()