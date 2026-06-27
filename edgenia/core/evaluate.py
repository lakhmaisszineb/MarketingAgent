from typing import Dict, Any
from langchain_groq import ChatGroq

class Evaluator:
    """Module d'évaluation - Mesure les résultats et apprend"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)
    
    def evaluate_campaign(self, campaign_result: Dict, previous_context: Dict) -> Dict:
        """Évalue les résultats d'une campagne et propose des améliorations"""
        prompt = f"""
Analyse les résultats de cette campagne :

{ campaign_result }

Contexte précédent :
{ previous_context['company_profile'] }

Retourne un JSON avec :
{{
  "performance": "Bonne / Moyenne / À améliorer",
  "key_insights": ["insight 1", "insight 2"],
  "lessons_learned": ["leçon 1", "leçon 2"],
  "next_actions": ["action 1", "action 2"],
  "improvement_score": 75
}}
"""
        try:
            response = self.llm.invoke(prompt)
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                return eval(json_match.group(0))
        except:
            pass
        
        return {
            "performance": "Moyenne",
            "key_insights": ["Besoin de plus de données"],
            "lessons_learned": ["Personnalisation importante"],
            "next_actions": ["Améliorer le ciblage"],
            "improvement_score": 65
        }