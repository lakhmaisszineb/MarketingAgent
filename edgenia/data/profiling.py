import pandas as pd
from typing import Dict, Any, List
import json

class DataProfiler:
    """Analyse automatique et intelligente d'un dataset client"""
    
    def analyze_dataset(self, file_path: str) -> Dict[str, Any]:
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Format non supporté (CSV ou Excel)")

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
                "recommendations": [],
                "data_quality_score": self._calculate_quality_score(df)
            }

            # Statistiques numériques
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                report["basic_stats"]["numeric"] = df[numeric_cols].describe().to_dict()

            # Valeurs uniques
            for col in df.columns:
                report["basic_stats"][col] = {
                    "unique_values": int(df[col].nunique()),
                    "missing_percentage": float(df[col].isnull().mean() * 100)
                }

            # Recommandations intelligentes
            if len(df) < 100:
                report["recommendations"].append("Dataset petit - résultats à prendre avec prudence")
            
            high_missing = [col for col, pct in report["basic_stats"].items() 
                          if isinstance(pct, dict) and pct.get("missing_percentage", 0) > 30]
            if high_missing:
                report["recommendations"].append(f"Colonnes avec beaucoup de données manquantes : {high_missing}")

            return report

        except Exception as e:
            return {"error": str(e)}

    def _detect_customer_columns(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Détection intelligente des colonnes clients"""
        columns = df.columns.str.lower()
        mapping = {
            "email": [col for col in df.columns if 'email' in col.lower()],
            "name": [col for col in df.columns if any(x in col.lower() for x in ['nom', 'name', 'prenom', 'first', 'last', 'client'])],
            "purchase_date": [col for col in df.columns if any(x in col.lower() for x in ['date', 'achat', 'purchase', 'order', 'vente'])],
            "revenue": [col for col in df.columns if any(x in col.lower() for x in ['montant', 'revenue', 'price', 'amount', 'total', 'ca'])],
            "phone": [col for col in df.columns if any(x in col.lower() for x in ['phone', 'tel', 'portable'])],
            "city": [col for col in df.columns if any(x in col.lower() for x in ['ville', 'city', 'location'])],
        }
        return mapping

    def _calculate_quality_score(self, df: pd.DataFrame) -> int:
        """Score de qualité du dataset"""
        score = 100
        missing_ratio = df.isnull().mean().mean() * 100
        score -= int(missing_ratio * 0.5)
        if len(df) < 50:
            score -= 30
        return max(0, min(100, score))