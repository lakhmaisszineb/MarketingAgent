import pandas as pd
from typing import Dict, Any
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

class SchemaMapper:
    """Mapping intelligent des colonnes avec LLM"""
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
    
    def generate_mapping(self, profiling_report: Dict, sector: str = "General") -> Dict[str, str]:
        columns = profiling_report["columns"]
        sample = profiling_report.get("sample_data", [{}])[0] if profiling_report.get("sample_data") else {}
        
        prompt = f"""
Secteur de l'entreprise : {sector}

Colonnes du dataset :
{columns}

Exemple de ligne :
{sample}

Mappe chaque colonne originale vers un nom standard en snake_case.
Noms standards prioritaires : email, full_name, last_purchase_date, total_revenue, city, phone, customer_status, etc.

Retourne uniquement un JSON valide.
"""
        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                mapping = json.loads(json_match.group(0))
                return mapping
        except Exception as e:
            print(f"Erreur LLM mapping: {e}")
        
        # Fallback
        return self._basic_mapping(columns)
    
    def _basic_mapping(self, columns: list) -> Dict[str, str]:
        mapping = {}
        for col in columns:
            lower = col.lower()
            if 'email' in lower:
                mapping[col] = 'email'
            elif any(x in lower for x in ['nom', 'name', 'prenom', 'client']):
                mapping[col] = 'full_name'
            elif any(x in lower for x in ['date', 'achat', 'purchase', 'visite']):
                mapping[col] = 'last_purchase_date'
            elif any(x in lower for x in ['montant', 'revenue', 'ca', 'amount']):
                mapping[col] = 'total_revenue'
            elif any(x in lower for x in ['ville', 'city']):
                mapping[col] = 'city'
            else:
                mapping[col] = col.lower().replace(' ', '_')
        return mapping