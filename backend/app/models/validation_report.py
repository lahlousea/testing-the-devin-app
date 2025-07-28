from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ValidationReport(Base):
    __tablename__ = "validation_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"))
    status = Column(String, default="processing")
    overall_score = Column(Float)
    recommendations = Column(Text)
    market_analysis = Column(Text)
    competition_analysis = Column(Text)
    risk_assessment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    startup = relationship("Startup", back_populates="validation_reports")
    hypotheses = relationship("Hypothesis", back_populates="report")
