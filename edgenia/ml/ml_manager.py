from typing import Dict, Any
import pandas as pd
from edgenia.ml.churn_predictor import ChurnPredictor
from edgenia.ml.segmentation import CustomerSegmenter
from edgenia.ml.next_purchase import NextPurchasePredictor
from edgenia.ml.rfm import RFMAnalyzer
from edgenia.ml.clv_calculator import CLVCalculator

class MLManager:
    """Manager central pour tous les modèles ML"""
    
    def __init__(self):
        self.churn = ChurnPredictor()
        self.segmenter = CustomerSegmenter(n_clusters=4)
        self.next_purchase = NextPurchasePredictor()
        self.rfm = RFMAnalyzer()
        self.clv = CLVCalculator()
    
    def analyze_customer_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse complète avec tous les modèles"""
        results = {}
        
        # RFM
        results["rfm"] = self.rfm.analyze(df)
        
        # Segmentation
        results["segmentation"] = self.segmenter.segment(df)
        
        # CLV
        results["clv"] = self.clv.calculate_clv(df)
        
        # Churn (si colonne churn existe, sinon simulation)
        if 'churn' in df.columns:
            results["churn"] = self.churn.predict_churn(df)
        else:
            results["churn"] = {"note": "Modèle churn non entraîné - besoin de colonne churn"}
        
        return results