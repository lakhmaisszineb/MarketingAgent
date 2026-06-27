from typing import Dict, Any
from edgenia.core.company import CompanyManager
from edgenia.core.observe import Observer
from edgenia.core.analyze import Analyzer
from edgenia.core.reason import Reasoner
from edgenia.core.plan import Planner
from edgenia.core.execute import Executor
from edgenia.core.evaluate import Evaluator

class EdgeniaAgent:
    """
    Agent principal d'Edgenia - Version 1
    Orchestre tout le cycle autonome
    """
    
    def __init__(self, company_id: str = "default_company"):
        self.company_id = company_id
        self.company_manager = CompanyManager(company_id)
        
        # Modules de la boucle
        self.observer = Observer(self.company_manager)
        self.analyzer = Analyzer()
        self.reasoner = Reasoner()
        self.planner = Planner()
        self.executor = Executor()
        self.evaluator = Evaluator()
    
    def initialize_company(self, onboarding_responses: Dict, data_file_path: str) -> Dict:
        """Phase 1 : Initialisation complète de l'entreprise"""
        print(f"Initialisation de l'entreprise {onboarding_responses.get('1', '')}...")
        result = self.company_manager.full_onboarding_and_data_processing(
            onboarding_responses, data_file_path
        )
        print("Initialisation terminée avec succès.\n")
        return result
    
    def run_cycle(self) -> Dict:
        """Exécute un cycle complet de raisonnement"""
        print("Démarrage d'un nouveau cycle d'analyse...\n")
        
        # 1. Observation
        observation = self.observer.observe()
        print("Observation terminée.")
        
        # 2. Analyse
        analysis = self.analyzer.analyze(observation, self.company_manager.memory.get_full_context())
        print("Analyse terminée.")
        
        # 3. Raisonnement
        reasoning = self.reasoner.reason(observation, analysis, self.company_manager.memory.get_full_context())
        print("Raisonnement terminé.")
        
        # 4. Planification
        plan = self.planner.generate_plan(observation, analysis, self.company_manager.memory.get_full_context())
        print("Plan d'action généré.")
        
        # 5. Exécution (génération de contenu)
        if plan.get("short_term_plan"):
            first_action = plan["short_term_plan"][0]
            content = self.executor.generate_email(first_action, self.company_manager.memory.get_full_context())
            print("Contenu généré (email prêt).")
        
        # 6. Évaluation (simulation)
        simulated_result = {"open_rate": 22, "click_rate": 5.5}
        evaluation = self.evaluator.evaluate(simulated_result, self.company_manager.memory.get_full_context())
        print("Évaluation terminée.\n")
        
        return {
            "observation": observation,
            "analysis": analysis,
            "reasoning": reasoning,
            "plan": plan,
            "evaluation": evaluation,
            "status": "cycle_completed"
        }
    
    def get_status(self) -> Dict:
        """Retourne l'état actuel de l'entreprise"""
        return self.company_manager.memory.get_full_context()