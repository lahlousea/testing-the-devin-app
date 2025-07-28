from typing import List, Dict
import re

class ValidationAnalyzer:
    def __init__(self):
        self.positive_indicators = [
            "love", "amazing", "great", "excellent", "perfect", "awesome", "fantastic",
            "helpful", "useful", "valuable", "needed", "essential", "game-changer",
            "revolutionary", "innovative", "successful", "profitable", "growing"
        ]
        
        self.negative_indicators = [
            "hate", "terrible", "awful", "useless", "waste", "failed", "failing",
            "problem", "issue", "bug", "broken", "difficult", "complicated",
            "expensive", "overpriced", "unnecessary", "redundant"
        ]
        
        self.credibility_sources = {
            "reddit": 0.7,
            "hackernews": 0.8,
            "techcrunch": 0.9,
            "producthunt": 0.8,
            "medium": 0.6,
            "blog": 0.5,
            "forum": 0.6
        }
    
    def analyze_evidence(self, evidence_list: List[Dict]) -> Dict:
        if not evidence_list:
            return {
                "overall_sentiment": 0.0,
                "evidence_strength": "weak",
                "validation_score": 0.3,
                "key_insights": ["Insufficient evidence found for validation"],
                "recommendations": ["Conduct primary market research", "Create MVP for direct user feedback"]
            }
        
        sentiment_scores = []
        relevance_scores = []
        credibility_scores = []
        
        for evidence in evidence_list:
            sentiment = self._calculate_sentiment(evidence["content"])
            relevance = self._calculate_relevance(evidence["content"])
            credibility = self._calculate_credibility(evidence["source"])
            
            sentiment_scores.append(sentiment)
            relevance_scores.append(relevance)
            credibility_scores.append(credibility)
            
            evidence["sentiment_score"] = sentiment
            evidence["relevance_score"] = relevance
            evidence["credibility_score"] = credibility
        
        overall_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        avg_relevance = sum(relevance_scores) / len(relevance_scores)
        avg_credibility = sum(credibility_scores) / len(credibility_scores)
        
        validation_score = (overall_sentiment + avg_relevance + avg_credibility) / 3
        
        evidence_strength = self._determine_evidence_strength(validation_score, len(evidence_list))
        key_insights = self._extract_key_insights(evidence_list)
        recommendations = self._generate_recommendations(validation_score, evidence_strength)
        
        return {
            "overall_sentiment": overall_sentiment,
            "evidence_strength": evidence_strength,
            "validation_score": validation_score,
            "key_insights": key_insights,
            "recommendations": recommendations,
            "evidence_count": len(evidence_list)
        }
    
    def _calculate_sentiment(self, content: str) -> float:
        content_lower = content.lower()
        positive_count = sum(1 for word in self.positive_indicators if word in content_lower)
        negative_count = sum(1 for word in self.negative_indicators if word in content_lower)
        
        if positive_count > negative_count:
            base_sentiment = 0.5
        elif negative_count > positive_count:
            base_sentiment = -0.5
        else:
            base_sentiment = 0.0
        
        total_words = len(content_lower.split())
        sentiment_strength = min(1.0, (positive_count + negative_count) / max(1, total_words / 10))
        
        final_sentiment = base_sentiment * sentiment_strength
        return max(-1, min(1, final_sentiment))
    
    def _calculate_relevance(self, content: str) -> float:
        relevance_keywords = [
            "startup", "business", "product", "market", "customer", "user",
            "revenue", "growth", "scale", "competition", "solution", "problem"
        ]
        
        content_lower = content.lower()
        relevance_score = sum(1 for keyword in relevance_keywords if keyword in content_lower)
        
        return min(1.0, relevance_score / 5)
    
    def _calculate_credibility(self, source: str) -> float:
        source_lower = source.lower()
        
        for source_type, score in self.credibility_sources.items():
            if source_type in source_lower:
                return score
        
        return 0.5
    
    def _determine_evidence_strength(self, validation_score: float, evidence_count: int) -> str:
        if validation_score >= 0.7 and evidence_count >= 5:
            return "strong"
        elif validation_score >= 0.5 and evidence_count >= 3:
            return "moderate"
        else:
            return "weak"
    
    def _extract_key_insights(self, evidence_list: List[Dict]) -> List[str]:
        insights = []
        
        positive_evidence = [e for e in evidence_list if e.get("sentiment_score", 0) > 0.3]
        negative_evidence = [e for e in evidence_list if e.get("sentiment_score", 0) < -0.3]
        
        if positive_evidence:
            insights.append(f"Found {len(positive_evidence)} positive validation points")
        
        if negative_evidence:
            insights.append(f"Identified {len(negative_evidence)} potential concerns or challenges")
        
        high_credibility = [e for e in evidence_list if e.get("credibility_score", 0) > 0.7]
        if high_credibility:
            insights.append(f"Evidence includes {len(high_credibility)} high-credibility sources")
        
        return insights[:5]
    
    def _generate_recommendations(self, validation_score: float, evidence_strength: str) -> List[str]:
        recommendations = []
        
        if validation_score < 0.4:
            recommendations.extend([
                "Consider pivoting the core value proposition",
                "Conduct deeper customer discovery interviews",
                "Validate problem-solution fit before building"
            ])
        elif validation_score < 0.6:
            recommendations.extend([
                "Test key assumptions with a minimal viable product",
                "Gather more direct customer feedback",
                "Refine target customer segments"
            ])
        else:
            recommendations.extend([
                "Proceed with MVP development",
                "Focus on customer acquisition strategies",
                "Plan for scaling and growth"
            ])
        
        if evidence_strength == "weak":
            recommendations.append("Increase market research and validation efforts")
        
        return recommendations[:5]
