import pandas as pd
from typing import Dict, Any
from sklearn.ensemble import RandomForestRegressor
from edgenia.ml.preprocessor import DataPreprocessor

class NextPurchasePredictor:
    """Prédiction du montant du prochain achat"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.preprocessor = DataPreprocessor()
        self.is_trained = False
        self.feature_names = None
        self.target_col = None
    
    def train(self, df: pd.DataFrame, target_col: str = 'next_purchase_amount') -> float:
        """Entraîne le modèle"""
        self.target_col = target_col
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        X = self.preprocessor.preprocess(X, target_col=self.target_col)
        self.feature_names = X.columns.tolist()
        
        self.model.fit(X, y)
        self.is_trained = True
        
        score = self.model.score(X, y)
        return score
    
    def predict_next_purchase(self, df: pd.DataFrame) -> Dict:
        """Prédit le montant du prochain achat"""
        if not self.is_trained:
            return {"error": "Modèle non entraîné"}
        
        X = df.drop(columns=[self.target_col], errors='ignore') if self.target_col else df.copy()
        X = self.preprocessor.preprocess(X, target_col=self.target_col)
        X = X.reindex(columns=self.feature_names, fill_value=0)
        
        predictions = self.model.predict(X)
        
        return {
            "next_purchase_predictions": predictions.tolist(),
            "average_next_purchase": round(float(predictions.mean()), 2)
        }