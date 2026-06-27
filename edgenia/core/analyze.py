from typing import Dict, Any, List
from langchain_groq import ChatGroq

class Analyzer:
    """Module d'analyse - Détecte problèmes et opportunités"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
    
    def analyze(self, observation: Dict, company_context: Dict) -> Dict[str, Any]:
        """Analyse intelligente des observations"""
        prompt = f"""
Tu es un analyste marketing expert.

**Contexte de l'entreprise :**
{company_context['company_profile']}

**Observation actuelle :**
{observation}

Analyse la situation et retourne uniquement un JSON avec :
{{
  "strengths": ["point fort 1", "point fort 2"],
  "weaknesses": ["problème 1", "problème 2"],
  "opportunities": ["opportunité 1", "opportunité 2"],
  "priority_actions": ["action 1", "action 2"],
  "summary": "Résumé court en une phrase"
}}
"""
        try:
            response = self.llm.invoke(prompt)
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                return eval(json_match.group(0))  # temporaire, on améliorera le parsing plus tard
        except:
            pass
        
        # Fallback
        return {
            "strengths": ["Données clients disponibles"],
            "weaknesses": ["Dataset encore petit"],
            "opportunities": ["Personnalisation des campagnes"],
            "priority_actions": ["Segmenter les clients", "Créer première campagne email"],
            "summary": "Base saine pour commencer les actions marketing."
        }