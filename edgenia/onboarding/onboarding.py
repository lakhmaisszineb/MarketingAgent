from typing import Dict, Any, List
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
import re

load_dotenv()

class OnboardingManager:
    """Gère l'onboarding intelligent d'une nouvelle entreprise"""
    
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.4
        )
    
    def get_questionnaire(self) -> List[Dict]:
        """Questionnaire intelligent avec options quand pertinent"""
        return [
            {
                "id": 1,
                "question": "Quel est le nom de votre entreprise ?",
                "type": "text",
                "required": True
            },
            {
                "id": 2,
                "question": "Quel est votre secteur d'activité principal ?",
                "type": "select",
                "options": [
                    "Mode & Vêtements", "Beauté & Cosmétique", "Alimentation & Restaurant",
                    "Électronique", "Immobilier", "Éducation", "Santé", "Services", "Autre"
                ],
                "required": True
            },
            {
                "id": 3,
                "question": "Quels sont vos principaux objectifs marketing actuellement ? (choisissez plusieurs si besoin)",
                "type": "multiselect",
                "options": [
                    "Augmenter les ventes", "Acquérir de nouveaux clients",
                    "Fidéliser les clients existants", "Réactiver les clients inactifs",
                    "Améliorer l'image de marque", "Lancer de nouveaux produits"
                ],
                "required": True
            },
            {
                "id": 4,
                "question": "Quels canaux utilisez-vous principalement pour communiquer avec vos clients ?",
                "type": "multiselect",
                "options": ["Email", "Instagram", "Facebook", "WhatsApp", "TikTok", "LinkedIn", "SMS", "Site Web"],
                "required": True
            },
            {
                "id": 5,
                "question": "Décrivez brièvement votre client idéal (persona principal)",
                "type": "textarea",
                "required": False
            },
            {
                "id": 6,
                "question": "Quels sont vos plus grands défis marketing en ce moment ?",
                "type": "textarea",
                "required": True
            }
        ]
    
    def process_responses(self, responses: Dict) -> Dict[str, Any]:
        """Analyse les réponses avec le LLM pour créer un Company Profile riche"""
        prompt = f"""
Tu es un consultant marketing senior. Analyse les réponses suivantes d'onboarding :

{json.dumps(responses, indent=2, ensure_ascii=False)}

Crée un **Company Profile** professionnel et retourne uniquement un JSON valide avec cette structure :

{{
  "company_name": "...",
  "sector": "...",
  "main_objectives": ["...", "..."],
  "channels": ["...", "..."],
  "customer_persona": "Description courte...",
  "challenges": ["...", "..."],
  "initial_recommendations": ["Recommandation 1", "Recommandation 2"],
  "data_readiness": "Commentaires sur les données fournies"
}}
"""
        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                profile = json.loads(json_match.group(0))
                return profile
        except Exception as e:
            print(f"Erreur lors de l'analyse LLM: {e}")
        
        # Fallback
        return {
            "company_name": responses.get("1", "Entreprise"),
            "sector": responses.get("2", "Non spécifié"),
            "main_objectives": responses.get("3", ["Augmenter les ventes"]),
            "channels": responses.get("4", ["Email"]),
            "customer_persona": responses.get("5", ""),
            "challenges": [responses.get("6", "Non spécifié")],
            "initial_recommendations": ["Analyser les données clients", "Segmenter la base"],
            "data_readiness": "Prêt pour l'analyse"
        }