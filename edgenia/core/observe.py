from typing import Dict, Any
import pandas as pd
from edgenia.core.company import CompanyManager

class Observer:
    """Module d'observation - Extraction des KPIs"""
    
    def __init__(self, company_manager: CompanyManager):
        self.company_manager = company_manager
        self.context = company_manager.memory.get_full_context()
    
    def observe(self) -> Dict[str, Any]:
        """Observation complète avec KPIs"""
        data_summary = self.context.get("data_summary", {})
        mapping = self.context.get("column_mapping", {})
        
        kpis = {
            "total_customers": data_summary.get("rows", 0),
            "has_email": "email" in str(mapping.values()).lower(),
            "has_purchase_date": any("date" in str(k).lower() or "achat" in str(k).lower() for k in mapping.keys()),
            "has_revenue": any("montant" in str(k).lower() or "revenue" in str(k).lower() for k in mapping.keys()),
            "active_customers": self._estimate_active_customers(data_summary),
            "avg_revenue_per_customer": self._estimate_avg_revenue(data_summary)
        }
        
        observation = {
            "company_name": self.context["company_profile"].get("company_name"),
            "sector": self.context["company_profile"].get("sector"),
            "kpis": kpis,
            "recent_activity": "Aucune campagne lancée",
            "timestamp": "Maintenant",
            "data_quality": "Moyenne" if kpis["total_customers"] < 100 else "Bonne"
        }
        
        return observation
    
    def _estimate_active_customers(self, data_summary: Dict) -> int:
        """Estimation simple des clients actifs"""
        total = data_summary.get("rows", 0)
        return int(total * 0.65)  # estimation temporaire
    
    def _estimate_avg_revenue(self, data_summary: Dict) -> float:
        """Estimation simple du panier moyen"""
        return 450.0  # valeur par défaut temporaire