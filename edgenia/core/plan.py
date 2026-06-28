from typing import Dict, Any
from langchain_groq import ChatGroq
from edgenia.core.reason import Reasoner

class Planner:
    """Module de planification structurée"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
        self.reasoner = Reasoner()
    
    def generate_plan(self, observation: Dict, analysis: Dict, company_context: Dict) -> Dict[str, Any]:
        reasoning = self.reasoner.reason(observation, analysis, company_context)
        
        prompt = f"""
Contexte entreprise : {company_context.get('company_profile', {})}

Observation : {observation}
Analyse : {analysis}

Génère un plan d'action réaliste pour les 15 prochains jours.
Retourne uniquement un JSON avec cette structure exacte :
{{
  "short_term_plan": [
    {{"action": "Nom de l'action", "priority": "high/medium/low", "channel": "Email/Instagram", "expected_impact": "Description courte"}}
  ],
  "key_metrics_to_track": ["Open Rate", "Conversion Rate", "Engagement"],
  "overall_strategy": "Stratégie globale en une phrase"
}}
"""
        try:
            response = self.llm.invoke(prompt)
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                plan = eval(json_match.group(0))
                plan["reasoning"] = reasoning
                return plan
        except:
            pass
        
        # Fallback fiable
        return {
            "short_term_plan": [
                {"action": "Segmenter les clients", "priority": "high", "channel": "Internal", "expected_impact": "Meilleure personnalisation"},
                {"action": "Lancer première campagne email", "priority": "high", "channel": "Email", "expected_impact": "Augmentation de l'engagement"}
            ],
            "key_metrics_to_track": ["Open Rate", "Click Rate", "Conversion Rate"],
            "overall_strategy": "Commencer par la personnalisation basée sur les données clients",
            "reasoning": reasoning
        }