from typing import Dict, Any
from langchain_groq import ChatGroq
from edgenia.core.reason import Reasoner

class Planner:
    """Module de planification avancé"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
        self.reasoner = Reasoner()
    
    def generate_plan(self, observation: Dict, analysis: Dict, company_context: Dict) -> Dict[str, Any]:
        """Génère un plan d'action avec raisonnement"""
        reasoning = self.reasoner.reason(observation, analysis, {})
        
        prompt = f"""
Raisonnement :
{reasoning.get('reasoning_summary', '')}

Contexte entreprise :
{company_context['company_profile']}

Analyse :
{analysis}

Génère un plan d'action réaliste pour les 15 prochains jours.
Retourne uniquement un JSON.
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
        
        return {
            "short_term_plan": [],
            "key_metrics_to_track": [],
            "overall_strategy": "Améliorer la personnalisation",
            "reasoning": reasoning
        }