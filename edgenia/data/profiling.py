import pandas as pd
from typing import Dict, Any, List
import json

class DataProfiler:
    """Analyse automatique d'un dataset client (CSV ou Excel)"""
    
    def analyze_dataset(self, file_path: str) -> Dict[str, Any]:
        """
        Analyse complète d'un fichier de données client.
        Retourne un rapport détaillé.
        """
        try:
            # Charger le fichier (CSV ou Excel)
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Format de fichier non supporté. Utilisez CSV ou Excel.")

            report = {
                "file_name": file_path.split('/')[-1],
                "rows": len(df),
                "columns": list(df.columns),
                "column_count": len(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
                "data_types": df.dtypes.astype(str).to_dict(),
                "sample_data": df.head(5).to_dict(orient='records'),
                "basic_stats": {},
                "potential_customer_columns": self._detect_customer_columns(df),
                "recommendations": []
            }

            # Statistiques numériques
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                report["basic_stats"]["numeric"] = df[numeric_cols].describe().to_dict()

            # Valeurs uniques par colonne
            for col in df.columns:
                report["basic_stats"][col] = {
                    "unique_values": int(df[col].nunique()),
                    "missing_percentage": float(df[col].isnull().mean() * 100)
                }

            # Recommandations automatiques
            if len(df) < 100:
                report["recommendations"].append("Dataset assez petit. Les résultats peuvent manquer de précision.")
            
            high_missing = [col for col, pct in report["basic_stats"].items() 
                          if isinstance(pct, dict) and pct.get("missing_percentage", 0) > 30]
            if high_missing:
                report["recommendations"].append(f"Colonnes avec beaucoup de valeurs manquantes : {high_missing}")

            return report

        except Exception as e:
            return {"error": str(e)}

    def _detect_customer_columns(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Détecte les colonnes importantes (email, nom, date d'achat, etc.)"""
        columns = df.columns.str.lower()
        mapping = {
            "email": [col for col in df.columns if 'email' in col.lower()],
            "name": [col for col in df.columns if any(x in col.lower() for x in ['nom', 'name', 'prenom', 'first', 'last'])],
            "purchase_date": [col for col in df.columns if any(x in col.lower() for x in ['date', 'achat', 'purchase', 'order'])],
            "revenue": [col for col in df.columns if any(x in col.lower() for x in ['montant', 'revenue', 'price', 'amount', 'total'])],
            "phone": [col for col in df.columns if 'phone' in col.lower() or 'tel' in col.lower()],
        }
        return mapping
