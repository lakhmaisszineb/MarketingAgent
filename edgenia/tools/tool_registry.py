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
        """Appelle un outil externe (avec confirmation)"""
        if tool_name not in self.tools:
            return {"error": f"Outil '{tool_name}' non trouvé"}
        
        tool = self.tools[tool_name]
        
        print(f"L'agent veut utiliser : {tool_name}")
        print(f"Description : {tool['description']}")
        
        choice = input("Confirmer l'exécution ? (y/n): ").lower()
        
        if choice == 'y':
            try:
                result = tool["function"](**kwargs)
                print(f"Outil {tool_name} exécuté.")
                return result
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"status": "cancelled"}