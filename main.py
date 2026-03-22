from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
import schemas
from typing import Optional

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
def get_applications(
    status: Optional[str] = None,
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(models.Application)
    
    # Use status query if availible
    if status is not None:
        query = query.filter(models.Application.status == status)
    
    # Sort by date    
    query = query.order_by(models.Application.date_applied.desc())
    
    # Pagination
    query = query.offset(skip).limit(limit)
    
    return query.all()

# Get by id - Fetch a specific job application
@app.get("/applications/{id}", response_model=schemas.ApplicationResponse)
def get_application(
    id: int, 
    db: Session = Depends(get_db)
):
    # Attempt to find the application in the database
    application = db.query(models.Application).filter(models.Application.id == id).first()
    
    # If not found, return error message
    if application is None:
        raise HTTPException(status_code=404, detail="Job application not found!")
    
    return application

# Put - Update a specific job application
@app.put("/applications/{id}", response_model=schemas.ApplicationResponse)
def update_application(
    id: int,
    updated_data: schemas.ApplicationCreate,
    db: Session = Depends(get_db)
):
    # Find the application from the database
    application = db.query(models.Application).filter(models.Application.id == id).first()
    
    # If not found, return error message
    if application is None:
        raise HTTPException(status_code=404, detail="Job application not found!")
    
    # Update fields
    application.title = updated_data.title
    application.company = updated_data.company
    application.status = updated_data.status
    application.notes = updated_data.notes
    
    db.commit()
    db.refresh(application)
    
    return application

# Patch - Update specific fields in a job application
@app.patch("/applications/{id}", response_model=schemas.ApplicationResponse)
def update_application_partial(
    id: int,
    updated_data: schemas.ApplicationUpdate,
    db: Session = Depends(get_db)
):
    application = db.query(models.Application).filter(models.Application.id == id).first()

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    # Only update the fields necessary
    if updated_data.title is not None:
        application.title = updated_data.title

    if updated_data.company is not None:
        application.company = updated_data.company

    if updated_data.status is not None:
        application.status = updated_data.status

    if updated_data.notes is not None:
        application.notes = updated_data.notes

    db.commit()
    db.refresh(application)

    return application

# Delete - Remove a specific job application
@app.delete("/applications/{id}")
def delete_application(id: int, db: Session = Depends(get_db)):
    
    # Find the application from the database
    application = db.query(models.Application).filter(models.Application.id == id).first()
    
    # If not found, return error message
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(application)
    db.commit()
    
    return {"message": "Job application deleted!"}

# Default route
@app.get("/")
def root():
    return {"message": "Job Tracker is running!"}