from typing import Dict, List
import json

class HypothesisGenerator:
    def __init__(self):
        self.hypothesis_templates = {
            "value": [
                "Customers will find value in {value_proposition} because it solves {problem}",
                "The target market of {target_customers} has a strong need for {key_features}",
                "Users will pay for {value_proposition} instead of using free alternatives"
            ],
            "growth": [
                "Customers will discover this product through {acquisition_channel}",
                "Word-of-mouth will be strong because {value_proposition} creates significant impact",
                "The product will achieve viral growth through {viral_mechanism}"
            ],
            "viability": [
                "The {business_model} model will generate sustainable revenue in {industry}",
                "Customer acquisition cost will be lower than lifetime value due to {competitive_advantages}",
                "The market size of {market_indicators} supports a viable business"
            ],
            "feasibility": [
                "The technical implementation of {key_features} is achievable with current technology",
                "The team can build and scale {value_proposition} within reasonable timeframes",
                "Required resources for {business_model} are accessible and affordable"
            ]
        }
        
        self.industry_specific_hypotheses = {
            "saas": {
                "value": ["Users will adopt this SaaS solution because it integrates better with existing workflows"],
                "growth": ["SaaS customers will upgrade to higher tiers as they see ROI"],
                "viability": ["Monthly recurring revenue will be sustainable with low churn rates"]
            },
            "ecommerce": {
                "value": ["Customers will choose this marketplace over competitors due to better selection"],
                "growth": ["Sellers will join the platform because of lower fees or better tools"],
                "viability": ["Transaction volume will grow as both buyers and sellers see value"]
            }
        }
    
    def generate_hypotheses(self, components: Dict) -> List[Dict]:
        hypotheses = []
        
        for hypothesis_type, templates in self.hypothesis_templates.items():
            for template in templates:
                hypothesis = self._fill_template(template, components)
                if hypothesis:
                    hypotheses.append({
                        "type": hypothesis_type,
                        "statement": hypothesis,
                        "confidence_score": self._calculate_confidence(hypothesis, components),
                        "validation_status": "untested"
                    })
        
        industry = components.get("industry", "general_tech")
        if industry in self.industry_specific_hypotheses:
            for hypothesis_type, templates in self.industry_specific_hypotheses[industry].items():
                for template in templates:
                    hypothesis = self._fill_template(template, components)
                    if hypothesis:
                        hypotheses.append({
                            "type": f"{hypothesis_type}_industry_specific",
                            "statement": hypothesis,
                            "confidence_score": self._calculate_confidence(hypothesis, components),
                            "validation_status": "untested"
                        })
        
        return hypotheses[:8]
    
    def _fill_template(self, template: str, components: Dict) -> str:
        try:
            filled_template = template
            
            replacements = {
                "{value_proposition}": components.get("value_proposition", "the core value proposition"),
                "{target_customers}": ", ".join(components.get("target_customers", ["target customers"])),
                "{key_features}": ", ".join(components.get("key_features", ["key features"])),
                "{business_model}": components.get("business_model", "business model"),
                "{industry}": components.get("industry", "the industry"),
                "{competitive_advantages}": ", ".join(components.get("competitive_advantages", ["competitive advantages"])),
                "{market_indicators}": ", ".join(components.get("market_size_indicators", ["market indicators"])),
                "{problem}": "the identified problem",
                "{acquisition_channel}": "digital marketing channels",
                "{viral_mechanism}": "user referrals and sharing"
            }
            
            for placeholder, replacement in replacements.items():
                if placeholder in filled_template:
                    filled_template = filled_template.replace(placeholder, replacement)
            
            return filled_template
        except Exception:
            return ""
    
    def _calculate_confidence(self, hypothesis: str, components: Dict) -> float:
        confidence = 0.5
        
        if components.get("target_customers"):
            confidence += 0.1
        if components.get("value_proposition") != "Value proposition not clearly identified":
            confidence += 0.1
        if components.get("business_model") != "business_model_unclear":
            confidence += 0.1
        if components.get("key_features"):
            confidence += 0.1
        if components.get("competitive_advantages"):
            confidence += 0.1
        
        return min(confidence, 0.9)
