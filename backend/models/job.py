from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import func
from db.database import Base

class StoryJob(Base):
    __tablename__ = "story_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(255), unique=True, index=True)
    session_id = Column(String(255), index=True) #person who created the job
    theme = Column(String(255))
    status = Column(String(255))
    story_id = Column(Integer, nullable=True)#foreign key to story table, but make it easier
    error = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)