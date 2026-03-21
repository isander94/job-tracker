from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Open a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
# Post - Create a job application
@app.post("/applications", response_model=schemas.ApplicationResponse)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db)
):
    # Create an SQLAlchemy object
    db_application = models.Application(
        title=application.title,
        company=application.company,
        status=application.status,
        notes=application.notes
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    return db_application

# Get - Fetch all job applications
@app.get("/applications", response_model=list[schemas.ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    applications = db.query(models.Application).all()
    return applications

# Default route
@app.get("/")
def root():
    return {"message": "Job Tracker is running!"}