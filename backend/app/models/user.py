from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    trial_reports_used = Column(Integer, default=0)
    trial_reports_limit = Column(Integer, default=1)
    
    startups = relationship("Startup", back_populates="owner")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
