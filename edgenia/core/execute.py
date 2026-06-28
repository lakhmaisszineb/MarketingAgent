from typing import Dict, Any
from langchain_groq import ChatGroq

class Executor:
    """Module d'exécution - Génère du contenu adapté au canal"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    def generate_content(self, action: Dict, company_context: Dict) -> Dict[str, str]:
        """Génère le bon type de contenu selon le canal"""
        channel = action.get("channel", "Email").lower()
        
        if "email" in channel or "mail" in channel:
            return self.generate_email(action, company_context)
        elif "instagram" in channel or "post" in channel or "social" in channel:
            return {"content": self.generate_social_post(action, company_context), "type": "social_post"}
        elif "blog" in channel or "wordpress" in channel:
            return {"content": self.generate_blog_post(action, company_context), "type": "blog"}
        else:
            return self.generate_email(action, company_context)  # default
    
    def generate_email(self, action: Dict, company_context: Dict) -> Dict[str, str]:
        prompt = f"""
Entreprise : {company_context['company_profile'].get('company_name')}
Secteur : {company_context['company_profile'].get('sector')}
Action : {action.get('action', '')}

Génère un email marketing professionnel en français.
Retourne un JSON avec 'subject' et 'body'.
"""
        response = self.llm.invoke(prompt)
        try:
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                return eval(json_match.group(0))
        except:
            pass
        return {"subject": "Offre spéciale", "body": "Bonjour...\n"}
    
    def generate_social_post(self, action: Dict, company_context: Dict) -> str:
        prompt = f"""
Entreprise : {company_context['company_profile'].get('company_name')}
Action : {action.get('action', '')}

Génère un post court et engageant pour Instagram en français.
"""
        response = self.llm.invoke(prompt)
        return response.content
    
    def generate_blog_post(self, action: Dict, company_context: Dict) -> str:
        prompt = f"""
Entreprise : {company_context['company_profile'].get('company_name')}
Action : {action.get('action', '')}

Génère un article de blog court pour WordPress en français.
"""
        response = self.llm.invoke(prompt)
        return response.content