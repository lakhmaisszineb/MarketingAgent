from typing import Dict, Any
import json
from datetime import datetime

class CompanyMemory:
    """Mémoire persistante d'une entreprise (contexte + historique)"""
    
    def __init__(self, company_id: str):
        self.company_id = company_id
        self.data = {
            "company_profile": {},
            "data_summary": {},
            "column_mapping": {},
            "interaction_history": [],
            "last_updated": None
        }
    
    def save_onboarding(self, profile: Dict):
        self.data["company_profile"] = profile
        self.data["last_updated"] = datetime.now().isoformat()
        print(f" Profil entreprise sauvegardé pour {self.company_id}")
    
    def save_data_analysis(self, analysis_result: Dict):
        self.data["data_summary"] = analysis_result.get("profiling_report", {})
        self.data["column_mapping"] = analysis_result.get("column_mapping", {})
        self.data["last_updated"] = datetime.now().isoformat()
        print(f" Analyse des données clients sauvegardée pour {self.company_id}")
    
    def get_full_context(self) -> Dict:
        """Retourne tout le contexte pour l'agent"""
        return self.data
    
    def add_interaction(self, action: str, details: str):
        self.data["interaction_history"].append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        })