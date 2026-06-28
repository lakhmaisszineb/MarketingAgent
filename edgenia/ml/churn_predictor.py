import pandas as pd
from typing import Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from edgenia.ml.preprocessor import DataPreprocessor

class ChurnPredictor:
    """Prédiction de churn (perte client)"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.preprocessor = DataPreprocessor()
        self.is_trained = False
    
    def train(self, df: pd.DataFrame, target_col: str = 'churn') -> float:
        """Entraîne le modèle"""
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        X = self.preprocessor.preprocess(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        return accuracy
    
    def predict_churn(self, df: pd.DataFrame, target_col: str = 'churn') -> Dict:
        """Prédit le churn pour chaque client"""
        if not self.is_trained:
            return {"error": "Modèle non entraîné"}
        
        X = df.drop(columns=[target_col]) if target_col in df.columns else df
        X = self.preprocessor.preprocess(X)
        
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[:, 1]
        
        return {
            "churn_predictions": predictions.tolist(),
            "churn_probabilities": probabilities.tolist()
        }