from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(Integer, primary_key=True, index=True)
    hypothesis_id = Column(Integer, ForeignKey("hypotheses.id"))
    source = Column(String, nullable=False)
    source_url = Column(String)
    content = Column(Text, nullable=False)
    sentiment_score = Column(Float)
    relevance_score = Column(Float)
    credibility_score = Column(Float)
    evidence_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    hypothesis = relationship("Hypothesis", back_populates="evidence")
