from pydantic import BaseModel
from datetime import datetime

# Schema used to create an application
class ApplicationCreate(BaseModel):
    title: str
    company: str
    status: str | None = "applied"
    notes: str | None = None

# Schema used to return data
class ApplicationResponse(BaseModel):
    id: int
    title: str
    company: str
    status: str
    notes: str | None
    date_applied: datetime
    
    class Config:
        from_attributes = True
        
# Schema used to update data
class ApplicationUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    status: str | None = None
    notes: str | None = None