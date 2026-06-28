import pandas as pd
from typing import Dict, Any

class CLVCalculator:
    """Calcul de la Valeur Client à Vie (Lifetime Value)"""
    
    def calculate_clv(self, df: pd.DataFrame) -> Dict:
        """
        Calcul simple de CLV
        Formule : CLV = (Montant moyen × Fréquence d'achat) × Durée de vie estimée
        """
        df = df.copy()
        
        # Calculs de base
        avg_revenue = df['montant_moyen'].mean() if 'montant_moyen' in df.columns else df['montant'].mean()
        avg_frequency = df['frequence_achat'].mean() if 'frequence_achat' in df.columns else 3
        avg_lifespan = 24  # 24 mois par défaut
        
        clv = avg_revenue * avg_frequency * avg_lifespan
        
        # CLV par client
        df['clv'] = df['montant_moyen'] * df['frequence_achat'] * avg_lifespan if 'montant_moyen' in df.columns else df['montant'] * avg_frequency * avg_lifespan
        
        return {
            "average_clv": round(clv, 2),
            "total_clv": round(df['clv'].sum(), 2),
            "clv_per_customer": df['clv'].tolist(),
            "high_value_customers": df[df['clv'] > df['clv'].quantile(0.75)].shape[0]
        }