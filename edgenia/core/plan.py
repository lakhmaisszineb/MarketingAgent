from typing import Dict, Any, List
from langchain_groq import ChatGroq

class Planner:
    """Module de planification - Génère des plans d'action concrets"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
    
    def generate_plan(self, analysis: Dict, company_context: Dict) -> Dict[str, Any]:
        """Génère un plan d'action priorisé"""
        prompt = f"""
Tu es un stratège marketing expert.

**Contexte de l'entreprise :**
{company_context['company_profile']}

**Analyse actuelle :**
{analysis}

Génère un plan d'action clair et réaliste pour les 7 prochains jours.
Retourne uniquement un JSON avec cette structure :

{{
  "short_term_plan": [
    {{"action": "Nom de l'action", "priority": "high/medium/low", "channel": "Email/Instagram/etc", "expected_impact": "Description courte"}}
  ],
  "key_metrics_to_track": ["Open Rate", "Conversion Rate", ...],
  "overall_strategy": "Résumé stratégique en une phrase"
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
        
        # Fallback
        return {
            "short_term_plan": [
                {"action": "Créer une première segmentation clients", "priority": "high", "channel": "Internal", "expected_impact": "Meilleure personnalisation"},
                {"action": "Lancer une campagne email de bienvenue", "priority": "high", "channel": "Email", "expected_impact": "Augmentation de l'engagement"}
            ],
            "key_metrics_to_track": ["Taux d'ouverture", "Taux de clics", "Taux de conversion"],
            "overall_strategy": "Commencer par la personnalisation basée sur les données clients existantes."
        }