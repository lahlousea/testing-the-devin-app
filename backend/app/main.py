from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
import asyncio
from typing import List

from .database import get_db, engine, Base
from .models import user, startup, validation_report, hypothesis, evidence, subscription
from .schemas import (
    UserCreate, UserResponse, Token, StartupCreate, StartupResponse,
    ValidationRequest, ValidationReportResponse, SubscriptionResponse
)
from .auth import get_current_user, verify_password, get_password_hash, create_access_token
from .ai import IdeaDecomposer, HypothesisGenerator, ValidationAnalyzer
from .scrapers import PerplexityScraper

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Startup Validation Platform", version="1.0.0")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

idea_decomposer = IdeaDecomposer()
hypothesis_generator = HypothesisGenerator()
validation_analyzer = ValidationAnalyzer()
perplexity_scraper = PerplexityScraper()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(user.User).filter(user.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_data.password)
    db_user = user.User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    db_subscription = subscription.Subscription(
        user_id=db_user.id,
        plan_type="free",
        reports_limit=1
    )
    db.add(db_subscription)
    db.commit()
    
    return db_user

@app.post("/api/auth/login", response_model=Token)
async def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(user.User).filter(user.User.email == email).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/startups", response_model=StartupResponse)
async def create_startup(
    startup_data: StartupCreate,
    current_user: user.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_startup = startup.Startup(
        name=startup_data.name,
        description=startup_data.description,
        industry=startup_data.industry,
        target_market=startup_data.target_market,
        business_model=startup_data.business_model,
        owner_id=current_user.id
    )
    db.add(db_startup)
    db.commit()
    db.refresh(db_startup)
    return db_startup

@app.post("/api/validate", response_model=dict)
async def validate_startup(
    validation_request: ValidationRequest,
    current_user: user.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_startup = db.query(startup.Startup).filter(
        startup.Startup.id == validation_request.startup_id,
        startup.Startup.owner_id == current_user.id
    ).first()
    
    if not db_startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    user_subscription = db.query(subscription.Subscription).filter(
        subscription.Subscription.user_id == current_user.id
    ).first()
    
    if not user_subscription:
        raise HTTPException(status_code=400, detail="No subscription found")
    
    unlimited_emails = ["sales@airwyz.com", "sales@aiwyz.com"]
    if current_user.email not in unlimited_emails and user_subscription.reports_used_this_period >= user_subscription.reports_limit:
        raise HTTPException(status_code=403, detail="Report limit exceeded")
    
    db_report = validation_report.ValidationReport(
        startup_id=db_startup.id,
        status="processing"
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    asyncio.create_task(process_validation_async(db_report.id, db_startup.description))
    
    unlimited_emails = ["sales@airwyz.com", "sales@aiwyz.com"]
    if current_user.email not in unlimited_emails:
        user_subscription.reports_used_this_period += 1
        db.commit()
    
    return {"report_id": db_report.id, "status": "processing"}

async def process_validation_async(report_id: int, startup_description: str):
    db = next(get_db())
    try:
        components = idea_decomposer.decompose_idea(startup_description)
        
        hypotheses_data = hypothesis_generator.generate_hypotheses(components)
        
        search_query = f"{components.get('value_proposition', '')} {components.get('industry', '')}"
        
        perplexity_results = perplexity_scraper.search_discussions(search_query)
        
        all_evidence = perplexity_results
        
        analysis_result = validation_analyzer.analyze_evidence(all_evidence)
        
        db_report = db.query(validation_report.ValidationReport).filter(
            validation_report.ValidationReport.id == report_id
        ).first()
        
        if db_report:
            db_report.status = "completed"
            db_report.overall_score = analysis_result["validation_score"]
            db_report.recommendations = json.dumps(analysis_result["recommendations"])
            db_report.market_analysis = json.dumps(analysis_result["key_insights"])
            db_report.completed_at = datetime.utcnow()
            
            for hyp_data in hypotheses_data:
                db_hypothesis = hypothesis.Hypothesis(
                    report_id=report_id,
                    type=hyp_data["type"],
                    statement=hyp_data["statement"],
                    confidence_score=hyp_data["confidence_score"],
                    validation_status=hyp_data["validation_status"]
                )
                db.add(db_hypothesis)
                db.commit()
                db.refresh(db_hypothesis)
                
                for evidence_item in all_evidence[:3]:
                    db_evidence = evidence.Evidence(
                        hypothesis_id=db_hypothesis.id,
                        source=evidence_item["source"],
                        source_url=evidence_item.get("source_url", ""),
                        content=evidence_item["content"][:1000],
                        sentiment_score=evidence_item.get("sentiment_score", 0.0),
                        relevance_score=evidence_item.get("relevance_score", 0.0),
                        credibility_score=evidence_item.get("credibility_score", 0.0)
                    )
                    db.add(db_evidence)
            
            db.commit()
    
    except Exception as e:
        print(f"Error processing validation: {e}")
        db_report = db.query(validation_report.ValidationReport).filter(
            validation_report.ValidationReport.id == report_id
        ).first()
        if db_report:
            db_report.status = "failed"
            db.commit()
    finally:
        db.close()

@app.get("/api/reports/{report_id}", response_model=ValidationReportResponse)
async def get_validation_report(
    report_id: int,
    current_user: user.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_report = db.query(validation_report.ValidationReport).filter(
        validation_report.ValidationReport.id == report_id
    ).join(startup.Startup).filter(
        startup.Startup.owner_id == current_user.id
    ).first()
    
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return db_report

@app.get("/api/user/usage", response_model=SubscriptionResponse)
async def get_user_usage(
    current_user: user.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_subscription = db.query(subscription.Subscription).filter(
        subscription.Subscription.user_id == current_user.id
    ).first()
    
    if not user_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return user_subscription

@app.get("/api/startups", response_model=List[StartupResponse])
async def get_user_startups(
    current_user: user.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_startups = db.query(startup.Startup).filter(
        startup.Startup.owner_id == current_user.id
    ).all()
    
    return user_startups
