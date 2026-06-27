from typing import Dict, Any
from langchain_groq import ChatGroq

class Executor:
    """Module d'exécution - Génère du contenu marketing concret"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.65)
    
    def generate_email(self, action: Dict, company_context: Dict, customer_segment: str = "all") -> Dict[str, str]:
        """Génère un email complet"""
        prompt = f"""
Entreprise : {company_context['company_profile'].get('company_name')}
Secteur : {company_context['company_profile'].get('sector')}
Action : {action.get('action', '')}

Génère un email marketing professionnel en français.
Retourne un JSON avec 'subject' et 'body'.
"""
        try:
            response = self.llm.invoke(prompt)
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                content = eval(json_match.group(0))
                return content
        except:
            pass
        
        return {
            "subject": "Découvrez nos nouvelles offres spéciales",
            "body": "Bonjour,\n\nNous avons préparé pour vous des offres exclusives..."
        }
    
    def generate_social_post(self, action: Dict, company_context: Dict) -> str:
        """Génère un post pour réseaux sociaux"""
        prompt = f"""
Entreprise : {company_context['company_profile'].get('company_name')}

Action : {action.get('action', '')}

Génère un post court, engageant et professionnel pour Instagram ou Facebook en français.
Inclut un appel à l'action clair.
"""
        response = self.llm.invoke(prompt)
        return response.content