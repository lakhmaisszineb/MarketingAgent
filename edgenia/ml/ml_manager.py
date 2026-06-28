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
        self.segmenter = CustomerSegmenter(n_clusters=3)
        self.next_purchase = NextPurchasePredictor()
        self.rfm = RFMAnalyzer()
        self.clv = CLVCalculator()
    
    def analyze_customer_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse complète avec tous les modèles (robuste aux colonnes manquantes)"""
        results = {}
        
        try:
            results["rfm"] = self.rfm.analyze(df)
        except:
            results["rfm"] = {"note": "RFM non disponible - colonnes manquantes"}
        
        try:
            results["segmentation"] = self.segmenter.segment(df)
        except:
            results["segmentation"] = {"note": "Segmentation non disponible"}
        
        try:
            results["clv"] = self.clv.calculate_clv(df)
        except:
            results["clv"] = {"note": "CLV non disponible"}
        
        results["churn"] = {"note": "Modèle churn non entraîné - besoin de colonne churn"}
        
        return results