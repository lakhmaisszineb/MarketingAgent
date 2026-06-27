import pandas as pd
from typing import Dict, Any
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

class SchemaMapper:
    """Mapping intelligent des colonnes vers un standard grâce au LLM"""
    
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2   # plus déterministe
        )
    
    def generate_mapping(self, profiling_report: Dict[str, Any], sector: str = "General") -> Dict[str, str]:
        """
        Mapping intelligent utilisant le LLM + contexte métier.
        """
        columns = profiling_report["columns"]
        sample = profiling_report.get("sample_data", [{}])[0] if profiling_report.get("sample_data") else {}
        
        prompt = f"""
Tu es un expert senior en analyse de données clients pour le marketing.

**Contexte de l'entreprise :** {sector}

Colonnes disponibles :
{columns}

Exemple de donnée :
{sample}

Ta mission : Mapper chaque colonne originale vers un nom standard en snake_case.

Noms standards prioritaires :
- email, full_name, first_name, last_name, phone, city, country, age, gender
- last_purchase_date, purchase_count, total_revenue, average_order_value
- customer_status (vip, active, inactive, new, lost), segment

Retourne **uniquement** un JSON valide comme ceci, sans aucun texte avant ou après :
{{
  "nom de la colonne originale": "nom_standard",
  "autre colonne": "autre_standard"
}}

Exemple de réponse attendue :
{{
  "nom client": "full_name",
  "date dernier achat": "last_purchase_date"
}}
"""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            
            # Nettoyage robuste du JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                mapping = json.loads(json_str)
            else:
                mapping = self._basic_mapping(columns)
                
            return mapping
            
        except Exception as e:
            print(f"Erreur LLM mapping: {e}")
            return self._basic_mapping(columns)
    
    def _basic_mapping(self, columns: list) -> Dict[str, str]:
        """Fallback simple"""
        mapping = {}
        for col in columns:
            lower = col.lower().strip()
            if 'email' in lower:
                mapping[col] = 'email'
            elif any(x in lower for x in ['nom', 'name', 'prenom', 'client']):
                mapping[col] = 'full_name'
            elif any(x in lower for x in ['date', 'achat', 'purchase', 'order']):
                mapping[col] = 'last_purchase_date'
            elif any(x in lower for x in ['montant', 'revenue', 'ca', 'amount', 'total']):
                mapping[col] = 'total_revenue'
            elif any(x in lower for x in ['ville', 'city', 'location']):
                mapping[col] = 'city'
            else:
                mapping[col] = col.lower().replace(' ', '_').replace('-', '_')
        return mapping
