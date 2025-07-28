from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base

class Hypothesis(Base):
    __tablename__ = "hypotheses"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("validation_reports.id"))
    type = Column(String, nullable=False)
    statement = Column(Text, nullable=False)
    confidence_score = Column(Float)
    validation_status = Column(String, default="untested")
    
    report = relationship("ValidationReport", back_populates="hypotheses")
    evidence = relationship("Evidence", back_populates="hypothesis")
