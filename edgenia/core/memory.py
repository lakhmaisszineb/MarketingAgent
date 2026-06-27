from typing import Dict, Any
import json
from datetime import datetime
from pathlib import Path

class CompanyMemory:
    """Mémoire persistante et intelligente d'une entreprise"""
    
    def __init__(self, company_id: str):
        self.company_id = company_id
        self.memory_dir = Path("memory")
        self.memory_dir.mkdir(exist_ok=True)
        self.file_path = self.memory_dir / f"{company_id}.json"
        self.data = self._load_memory()
    
    def _load_memory(self) -> Dict:
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "company_profile": {},
            "data_summary": {},
            "column_mapping": {},
            "interaction_history": [],
            "last_updated": None
        }
    
    def save(self):
        """Sauvegarde la mémoire sur disque"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def save_onboarding(self, profile: Dict):
        self.data["company_profile"] = profile
        self.save()
        print(f" Profil entreprise sauvegardé ({self.company_id})")
    
    def save_data_analysis(self, analysis_result: Dict):
        self.data["data_summary"] = analysis_result.get("profiling_report", {})
        self.data["column_mapping"] = analysis_result.get("column_mapping", {})
        self.save()
        print(f" Analyse des données sauvegardée ({self.company_id})")
    
    def get_full_context(self) -> Dict:
        return self.data
    
    def add_interaction(self, action: str, details: str):
        self.data["interaction_history"].append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        })
        self.save()