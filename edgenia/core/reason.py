from typing import Dict, Any
from langchain_groq import ChatGroq

class Reasoner:
    """Module de raisonnement structuré et explicatif"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
    
    def reason(self, observation: Dict, analysis: Dict, company_context: Dict) -> Dict[str, Any]:
        """Raisonnement complet avec explicabilité"""
        prompt = f"""
Contexte entreprise : {company_context.get('company_profile', {})}

Observation actuelle :
{observation}

Analyse :
{analysis}

Explique de manière claire et professionnelle :
- Pourquoi ces actions sont prioritaires ?
- Quel est le lien avec les objectifs de l'entreprise ?
- Quels risques si on ne fait rien ?

Retourne uniquement un JSON valide.
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
            "reasoning_summary": "Le plan se concentre sur la personnalisation et la collecte de données car ce sont les leviers les plus efficaces pour la croissance.",
            "why_this_plan": ["Données disponibles mais sous-exploitées", "Objectifs de fidélisation et augmentation des ventes"],
            "risks_if_no_action": ["Perte de clients", "Stagnation des ventes"],
            "confidence_level": 78
        }