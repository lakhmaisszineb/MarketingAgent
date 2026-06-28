from typing import Dict, Callable, Any

class ToolRegistry:
    """Registre des outils et agents externes"""
    
    def __init__(self):
        self.tools = {}
    
    def register(self, name: str, func: Callable, description: str):
        self.tools[name] = {
            "function": func,
            "description": description
        }
    
    def list_tools(self) -> Dict[str, str]:
        """Liste les outils disponibles"""
        return {name: info["description"] for name, info in self.tools.items()}
    
    def call(self, tool_name: str, **kwargs) -> Any:
        """Appelle un outil externe"""
        if tool_name not in self.tools:
            return {"error": f"Outil '{tool_name}' non trouvé"}
        
        tool = self.tools[tool_name]
        
        print(f"L'agent veut utiliser l'outil : {tool_name}")
        print(f"Description : {tool['description']}")
        
        choice = input("Confirmer l'exécution ? (y/n): ").lower()
        
        if choice == 'y':
            try:
                return tool["function"](**kwargs)
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"status": "cancelled", "message": "Action annulée par l'utilisateur"}