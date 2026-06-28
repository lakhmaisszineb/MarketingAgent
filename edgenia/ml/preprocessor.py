import pandas as pd
from typing import Dict, Any
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np

class DataPreprocessor:
    """Préprocesseur généraliste pour n'importe quel dataset client"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
    
    def preprocess(self, df: pd.DataFrame, target_col: str = None) -> pd.DataFrame:
        """Prépare les données pour le ML (exclut la cible si spécifiée)"""
        df = df.copy()
        
        # Colonnes à prétraiter (tout sauf la cible)
        feature_cols = df.columns.tolist()
        if target_col and target_col in feature_cols:
            feature_cols.remove(target_col)
        
        # Encodage des colonnes catégorielles
        for col in df[feature_cols].select_dtypes(include=['object']).columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
        
        # Normalisation des colonnes numériques (sauf cible)
        numeric_cols = df[feature_cols].select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
        
        return df
    
    def get_feature_importance(self, df: pd.DataFrame, target_col: str = None) -> Dict[str, float]:
        """Estimation de l'importance des features"""
        importance = {}
        numeric_df = df.select_dtypes(include=['number'])
        
        if target_col and target_col in numeric_df.columns:
            numeric_df = numeric_df.drop(columns=[target_col])
        
        for col in numeric_df.columns:
            importance[col] = float(numeric_df[col].std())
        
        return importance