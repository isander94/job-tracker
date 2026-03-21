from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

# Job application model
class Application(Base):
    __tablename__ = "applications"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    status = Column(String, default="applied")
    notes = Column(String, nullable=True)
    date_applied = Column(DateTime, default=datetime.now)