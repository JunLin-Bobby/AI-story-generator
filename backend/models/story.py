from sqlalchemy import Column, Integer, String, DateTime,ForeignKey ,Boolean,JSON
from sqlalchemy import func 
from sqlalchemy.orm import relationship

from db.database import Base

class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    session_id = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    nodes = relationship("StoryNode",back_populates="story")

class StoryNode(Base):
    __tablename__ = "story_nodes"
    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"),index=True)
    content = Column(String(255))
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_good_ending = Column(Boolean, default=False)
    options = Column(JSON, default=list)

    story = relationship("Story", back_populates="nodes")