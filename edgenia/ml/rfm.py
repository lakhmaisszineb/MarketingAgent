import pandas as pd
from typing import Dict, Any
from datetime import datetime

class RFMAnalyzer:
    """Analyse RFM (Recency, Frequency, Monetary)"""
    
    def _quantile_score(self, series: pd.Series, bins: int = 5, ascending: bool = True) -> pd.Series:
        """Calcule un score quantile sûr, même si les valeurs sont dupliquées."""
        rank_values = series.rank(method='first')
        n_bins = min(bins, len(rank_values))
        labels = list(range(1, n_bins + 1))
        if not ascending:
            labels = labels[::-1]
        if n_bins == 1:
            return pd.Series([labels[0]] * len(series), index=series.index)
        return pd.qcut(rank_values, n_bins, labels=labels, duplicates='drop')

    def analyze(self, df: pd.DataFrame, date_col: str = 'derniere_vente', amount_col: str = 'montant') -> Dict:
        """Calcule les scores RFM"""
        df = df.copy()
        
        # Recency (jours depuis dernier achat)
        today = datetime.now()
        df['recency'] = (today - pd.to_datetime(df[date_col])).dt.days
        
        # Frequency et Monetary
        rfm = df.groupby('email').agg({
            'recency': 'min',
            amount_col: ['count', 'sum']
        }).reset_index()
        
        rfm.columns = ['email', 'recency', 'frequency', 'monetary']
        
        # Scores (1-5)
        rfm['R_score'] = self._quantile_score(rfm['recency'], bins=5, ascending=False)
        rfm['F_score'] = self._quantile_score(rfm['frequency'], bins=5, ascending=True)
        rfm['M_score'] = self._quantile_score(rfm['monetary'], bins=5, ascending=True)
        
        rfm['RFM_score'] = rfm['R_score'].astype(int) * 100 + rfm['F_score'].astype(int) * 10 + rfm['M_score'].astype(int)
        
        return {
            "rfm_table": rfm.to_dict(orient='records'),
            "average_rfm": rfm['RFM_score'].mean(),
            "vip_customers": rfm[rfm['RFM_score'] > 400].shape[0]
        }