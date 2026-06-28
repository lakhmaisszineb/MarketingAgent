from typing import Dict, Any
from edgenia.agents.main_agent import EdgeniaAgent
from edgenia.tools.tool_registry import ToolRegistry

class Orchestrator:
    """Orchestrateur multi-agents"""
    
    def __init__(self):
        self.main_agent = EdgeniaAgent()
        self.tools = ToolRegistry()
    
    def process_request(self, user_request: str, company_data: Dict) -> Dict:
        """Traite une requête utilisateur et orchestre les agents"""
        # Simulation d'analyse
        plan = self.main_agent.run_cycle()
        
        # Si le plan contient une action qui nécessite un autre agent
        actions = plan.get("plan", {}).get("short_term_plan", [])
        
        for action in actions:
            channel = action.get("channel", "").lower()
            if "email" in channel:
                print("Appel de l'agent Email...")
                # Ici on appellera l'agent email des autres stagiaires
            elif "instagram" in channel or "post" in channel:
                print("Appel de l'agent Social Media...")
            elif "wordpress" in channel or "blog" in channel:
                print("Appel de l'agent WordPress...")
        
        return {
            "plan": plan,
            "status": "orchestrated"
        }