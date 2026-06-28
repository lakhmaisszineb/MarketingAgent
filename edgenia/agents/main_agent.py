from typing import Dict, Any
import logging
import pandas as pd
from edgenia.core.company import CompanyManager
from edgenia.core.observe import Observer
from edgenia.core.analyze import Analyzer
from edgenia.core.reason import Reasoner
from edgenia.core.plan import Planner
from edgenia.core.execute import Executor
from edgenia.core.evaluate import Evaluator
from edgenia.ml.ml_manager import MLManager
from edgenia.tools.tool_registry import ToolRegistry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EdgeniaAgent:
    def __init__(self, company_id: str = "default"):
        self.company_id = company_id
        self.company_manager = CompanyManager(company_id)
        self.ml_manager = MLManager()
        
        self.observer = Observer(self.company_manager)
        self.analyzer = Analyzer()
        self.reasoner = Reasoner()
        self.planner = Planner()
        self.executor = Executor()
        self.evaluator = Evaluator()
        
        self.tools = ToolRegistry()
        self._register_tools()
        
        logger.info(f"Agent Edgenia initialisé pour {company_id}")
    
    def _register_tools(self):
        self.tools.register("send_email", self.executor.generate_email, "Envoie un email")
        self.tools.register("publish_post", self.executor.generate_social_post, "Publie un post")
    
    def initialize(self, onboarding_responses: Dict, data_file_path: str) -> Dict:
        try:
            logger.info("Démarrage onboarding...")
            result = self.company_manager.full_onboarding_and_data_processing(onboarding_responses, data_file_path)
            logger.info("Onboarding terminé avec succès")
            return result
        except Exception as e:
            logger.error(f"Erreur onboarding: {e}")
            return {"status": "error", "message": str(e)}
    
    def run_cycle(self) -> Dict:
        try:
            logger.info("Début du cycle autonome")
            
            observation = self.observer.observe()
            analysis = self.analyzer.analyze(observation, self.company_manager.memory.get_full_context())
            reasoning = self.reasoner.reason(observation, analysis, self.company_manager.memory.get_full_context())
            plan = self.planner.generate_plan(observation, analysis, self.company_manager.memory.get_full_context())
            
            ml_results = self.ml_manager.analyze_customer_data(pd.DataFrame())  # simulation
            
            logger.info("Cycle terminé avec succès")
            return {"status": "success", "plan": plan, "ml_results": ml_results}
        except Exception as e:
            logger.error(f"Erreur dans le cycle: {e}")
            return {"status": "error", "message": str(e)}
    
    def chat(self, user_message: str) -> str:
        """Mode conversationnel simple"""
        try:
            # Simulation de réponse conversationnelle
            response = self.run_cycle()
            return f"Plan généré. {response.get('plan', {}).get('overall_strategy', 'Prêt à agir.')}"
        except Exception as e:
            return f"Erreur : {str(e)}"