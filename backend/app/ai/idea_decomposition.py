import re
import nltk
from textblob import TextBlob
from typing import Dict, List
import json

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class IdeaDecomposer:
    def __init__(self):
        self.industry_keywords = {
            "saas": ["software", "platform", "api", "cloud", "subscription", "dashboard", "analytics"],
            "ecommerce": ["marketplace", "store", "shopping", "retail", "product", "inventory", "payment"],
            "fintech": ["payment", "banking", "finance", "money", "transaction", "investment", "crypto"],
            "healthtech": ["health", "medical", "patient", "doctor", "healthcare", "wellness", "fitness"],
            "edtech": ["education", "learning", "student", "course", "training", "skill", "knowledge"]
        }
    
    def decompose_idea(self, description: str) -> Dict:
        blob = TextBlob(description)
        sentences = blob.sentences
        
        components = {
            "target_customers": self._extract_target_customers(description),
            "value_proposition": self._extract_value_proposition(description),
            "business_model": self._extract_business_model(description),
            "industry": self._detect_industry(description),
            "key_features": self._extract_key_features(description),
            "market_size_indicators": self._extract_market_indicators(description),
            "competitive_advantages": self._extract_competitive_advantages(description)
        }
        
        return components
    
    def _extract_target_customers(self, text: str) -> List[str]:
        customer_patterns = [
            r"for\s+([^,.]+)",
            r"targeting\s+([^,.]+)",
            r"helps\s+([^,.]+)",
            r"designed for\s+([^,.]+)"
        ]
        
        customers = []
        for pattern in customer_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            customers.extend([match.strip() for match in matches])
        
        return list(set(customers))[:3]
    
    def _extract_value_proposition(self, text: str) -> str:
        value_patterns = [
            r"solves?\s+([^,.]+)",
            r"helps?\s+([^,.]+)",
            r"enables?\s+([^,.]+)",
            r"provides?\s+([^,.]+)"
        ]
        
        for pattern in value_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        sentences = TextBlob(text).sentences
        if sentences:
            return str(sentences[0])
        
        return "Value proposition not clearly identified"
    
    def _extract_business_model(self, text: str) -> str:
        model_keywords = {
            "subscription": ["subscription", "monthly", "recurring", "saas"],
            "marketplace": ["marketplace", "commission", "transaction fee"],
            "freemium": ["freemium", "free tier", "premium"],
            "advertising": ["ads", "advertising", "sponsored"],
            "ecommerce": ["selling", "products", "retail", "store"]
        }
        
        text_lower = text.lower()
        for model, keywords in model_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return model
        
        return "business_model_unclear"
    
    def _detect_industry(self, text: str) -> str:
        text_lower = text.lower()
        industry_scores = {}
        
        for industry, keywords in self.industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                industry_scores[industry] = score
        
        if industry_scores:
            return max(industry_scores.keys(), key=lambda k: industry_scores[k])
        
        return "general_tech"
    
    def _extract_key_features(self, text: str) -> List[str]:
        feature_patterns = [
            r"features?\s+([^,.]+)",
            r"includes?\s+([^,.]+)",
            r"offers?\s+([^,.]+)",
            r"capabilities?\s+([^,.]+)"
        ]
        
        features = []
        for pattern in feature_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            features.extend([match.strip() for match in matches])
        
        return list(set(features))[:5]
    
    def _extract_market_indicators(self, text: str) -> List[str]:
        market_patterns = [
            r"\$[\d,]+\s*(?:million|billion|k)",
            r"[\d,]+\s*(?:million|billion)\s+(?:users|customers|people)",
            r"growing\s+(?:market|industry|sector)",
            r"[\d]+%\s+(?:growth|increase)"
        ]
        
        indicators = []
        for pattern in market_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            indicators.extend(matches)
        
        return indicators
    
    def _extract_competitive_advantages(self, text: str) -> List[str]:
        advantage_patterns = [
            r"(?:unique|different|better|faster|cheaper|easier)\s+([^,.]+)",
            r"competitive\s+advantage\s+([^,.]+)",
            r"differentiates?\s+([^,.]+)"
        ]
        
        advantages = []
        for pattern in advantage_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            advantages.extend([match.strip() for match in matches])
        
        return list(set(advantages))[:3]
