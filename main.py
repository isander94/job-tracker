from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Open a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Default route
@app.get("/")
def root():
    return {"message": "Job Tracker is running!"}