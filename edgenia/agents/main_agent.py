from typing import Dict, Any
import logging
from edgenia.core.company import CompanyManager
from edgenia.core.observe import Observer
from edgenia.core.analyze import Analyzer
from edgenia.core.reason import Reasoner
from edgenia.core.plan import Planner
from edgenia.core.execute import Executor
from edgenia.core.evaluate import Evaluator

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EdgeniaAgent:
    """
    Agent IA Autonome Principal - Edgenia
    Version 1 améliorée
    """
    
    def __init__(self, company_id: str = "default"):
        self.company_id = company_id
        self.company_manager = CompanyManager(company_id)
        
        self.observer = Observer(self.company_manager)
        self.analyzer = Analyzer()
        self.reasoner = Reasoner()
        self.planner = Planner()
        self.executor = Executor()
        self.evaluator = Evaluator()
        
        logger.info(f"Agent initialisé pour l'entreprise {company_id}")
    
    def initialize(self, onboarding_responses: Dict, data_file_path: str) -> Dict:
        """Initialise une nouvelle entreprise"""
        try:
            logger.info(f"Démarrage onboarding pour {onboarding_responses.get('1')}")
            result = self.company_manager.full_onboarding_and_data_processing(
                onboarding_responses, data_file_path
            )
            logger.info("Initialisation réussie")
            return result
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {e}")
            return {"error": str(e)}
    
    def run_cycle(self) -> Dict[str, Any]:
        """Exécute un cycle complet d'autonomie"""
        try:
            logger.info("Début d'un nouveau cycle")
            
            observation = self.observer.observe()
            analysis = self.analyzer.analyze(observation, self.company_manager.memory.get_full_context())
            reasoning = self.reasoner.reason(observation, analysis, self.company_manager.memory.get_full_context())
            plan = self.planner.generate_plan(observation, analysis, self.company_manager.memory.get_full_context())
            
            # Exécution du premier élément du plan
            if plan.get("short_term_plan"):
                first_action = plan["short_term_plan"][0]
                content = self.executor.generate_email(first_action, self.company_manager.memory.get_full_context())
            
            # Évaluation
            evaluation = self.evaluator.evaluate({"open_rate": 23}, self.company_manager.memory.get_full_context())
            
            logger.info("Cycle terminé avec succès")
            return {
                "status": "success",
                "observation": observation,
                "analysis": analysis,
                "reasoning": reasoning,
                "plan": plan,
                "evaluation": evaluation
            }
        except Exception as e:
            logger.error(f"Erreur pendant le cycle: {e}")
            return {"status": "error", "message": str(e)}