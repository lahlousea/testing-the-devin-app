from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    trial_reports_used: int
    trial_reports_limit: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class StartupCreate(BaseModel):
    name: str
    description: str
    industry: str
    target_market: Optional[str] = None
    business_model: Optional[str] = None

class StartupResponse(BaseModel):
    id: int
    name: str
    description: str
    industry: str
    target_market: Optional[str]
    business_model: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class HypothesisResponse(BaseModel):
    id: int
    type: str
    statement: str
    confidence_score: Optional[float]
    validation_status: str

    class Config:
        from_attributes = True

class EvidenceResponse(BaseModel):
    id: int
    source: str
    source_url: Optional[str]
    content: str
    sentiment_score: Optional[float]
    relevance_score: Optional[float]
    credibility_score: Optional[float]
    evidence_type: Optional[str]

    class Config:
        from_attributes = True

class ValidationReportResponse(BaseModel):
    id: int
    status: str
    overall_score: Optional[float]
    recommendations: Optional[str]
    market_analysis: Optional[str]
    competition_analysis: Optional[str]
    risk_assessment: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    startup: StartupResponse
    hypotheses: List[HypothesisResponse]

    class Config:
        from_attributes = True

class ValidationRequest(BaseModel):
    startup_id: int

class SubscriptionResponse(BaseModel):
    id: int
    plan_type: str
    status: str
    reports_used_this_period: int
    reports_limit: int
    current_period_end: Optional[datetime]

    class Config:
        from_attributes = True
