from typing import Dict, Any
from langchain_groq import ChatGroq

class Evaluator:
    """Module d'évaluation et d'amélioration continue"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)
    
    def evaluate(self, campaign_result: Dict, previous_context: Dict) -> Dict[str, Any]:
        """Évalue les résultats et propose des améliorations"""
        prompt = f"""
Résultats de campagne :
{campaign_result}

Contexte entreprise :
{previous_context.get('company_profile', {})}

Analyse les résultats et propose des améliorations.
Retourne uniquement un JSON :
{{
  "performance": "Bonne/Moyenne/À améliorer",
  "key_insights": ["insight 1", "insight 2"],
  "lessons_learned": ["leçon 1", "leçon 2"],
  "improvement_suggestions": ["suggestion 1", "suggestion 2"],
  "next_cycle_recommendation": "Recommandation pour le prochain cycle"
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
            "key_insights": ["Taux d'ouverture correct", "Taux de conversion à améliorer"],
            "lessons_learned": ["La personnalisation augmente l'engagement"],
            "improvement_suggestions": ["Tester différents sujets d'email", "Segmenter mieux l'audience"],
            "next_cycle_recommendation": "Améliorer la personnalisation et tester A/B"
        }