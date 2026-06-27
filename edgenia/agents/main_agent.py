from typing import Dict, Any
from edgenia.core.company import CompanyManager

class EdgeniaAgent:
    """Agent principal d'Edgenia - Orchestrateur central"""
    
    def __init__(self, company_id: str = "company_001"):
        self.company_id = company_id
        self.company_manager = CompanyManager(company_id)
    
    def initialize_company(self, onboarding_responses: Dict, customer_data_file: str) -> Dict:
        """
        Processus complet d'initialisation d'une nouvelle entreprise
        """
        print(f" Initialisation de l'entreprise {onboarding_responses.get('1', '')}...")
        
        result = self.company_manager.full_onboarding_and_data_processing(
            onboarding_responses, 
            customer_data_file
        )
        
        if "error" in result:
            print(f"Erreur : {result['error']}")
            return result
        
        print("\n Initialisation terminée avec succès.")
        return result
    
    def get_company_context(self) -> Dict:
        """Récupère tout le contexte de l'entreprise"""
        return self.company_manager.memory.get_full_context()