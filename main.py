from fastapi import FastAPI

app = FastAPI()

# Default route
@app.get("/")
def root():
    return {"message": "Job Tracker is running!"}