from typing import Dict, Any
from edgenia.onboarding.onboarding import OnboardingManager
from edgenia.data.profiling import DataProfiler
from edgenia.data.schema_mapper import SchemaMapper
from edgenia.core.memory import CompanyMemory
import json
from langchain_groq import ChatGroq

class CompanyManager:
    """Orchestrateur principal d'une entreprise"""
    
    def __init__(self, company_id: str = "company_001"):
        self.company_id = company_id
        self.memory = CompanyMemory(company_id)
        self.onboarding_mgr = OnboardingManager()
        self.profiler = DataProfiler()
        self.mapper = SchemaMapper()
    
    def full_onboarding_and_data_processing(self, onboarding_responses: Dict, data_file_path: str) -> Dict:
        """
        Processus complet : Onboarding → Analyse données → Mémoire → Rapport
        """
        # 1. Onboarding
        company_profile = self.onboarding_mgr.process_responses(onboarding_responses)
        self.memory.save_onboarding(company_profile)
        
        # 2. Analyse des données clients
        data_result = self.profiler.analyze_dataset(data_file_path)
        if "error" in data_result:
            return {"error": data_result["error"]}
        
        column_mapping = self.mapper.generate_mapping(data_result, sector=company_profile.get("sector", "General"))
        
        analysis_result = {
            "profiling_report": data_result,
            "column_mapping": column_mapping
        }
        self.memory.save_data_analysis(analysis_result)
        
        # 3. Générer un rapport de bienvenue
        welcome_report = self._generate_welcome_report(company_profile, data_result, column_mapping)
        
        return {
            "status": "success",
            "company_profile": company_profile,
            "data_analysis": analysis_result,
            "welcome_report": welcome_report,
            "memory": self.memory.get_full_context()
        }
    
    def _generate_welcome_report(self, profile: Dict, data_report: Dict, mapping: Dict) -> str:
        """Rapport intelligent de bienvenue"""
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6)
        
        prompt = f"""
Tu es Edgenia, un AI Growth Agent autonome.
L'entreprise {profile.get('company_name')} vient de compléter son onboarding.

Informations entreprise :
{json.dumps(profile, indent=2, ensure_ascii=False)}

Analyse de leurs données clients :
- {data_report.get('rows', 0)} clients
- Colonnes principales : {data_report.get('columns', [])}
- Mapping détecté : {mapping}

Génère un message de bienvenue professionnel, clair et stratégique (maximum 250 mots).
Montre que tu as bien compris leur métier et leurs données.
Propose les prochaines étapes concrètes.
"""
        response = llm.invoke(prompt)
        return response.content