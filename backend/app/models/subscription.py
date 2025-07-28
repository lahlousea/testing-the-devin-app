from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_type = Column(String, default="free")
    stripe_subscription_id = Column(String)
    status = Column(String, default="active")
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    reports_used_this_period = Column(Integer, default=0)
    reports_limit = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="subscription")
