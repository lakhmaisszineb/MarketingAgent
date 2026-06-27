from typing import Dict, Any
from langchain_groq import ChatGroq

class Executor:
    """Module d'exécution - Génère du contenu concret"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    def generate_email(self, plan_action: Dict, company_context: Dict) -> str:
        """Génère un email marketing personnalisé"""
        prompt = f"""
Entreprise : {company_context['company_profile'].get('company_name')}
Secteur : {company_context['company_profile'].get('sector')}

Action à exécuter : {plan_action.get('action')}

Génère un email marketing professionnel, persuasif et adapté au public cible.
Inclut un objet (subject) clair et un corps d'email.
"""
        response = self.llm.invoke(prompt)
        return response.content
    
    def generate_social_post(self, plan_action: Dict, company_context: Dict) -> str:
        """Génère un post pour réseaux sociaux"""
        prompt = f"""
Entreprise : {company_context['company_profile'].get('company_name')}

Action : {plan_action.get('action')}

Génère un post engageant pour Instagram ou Facebook.
Court, attractif, avec appel à l'action.
"""
        response = self.llm.invoke(prompt)
        return response.content