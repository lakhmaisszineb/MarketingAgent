import pandas as pd
from typing import Dict, Any
from sklearn.cluster import KMeans
from langchain_groq import ChatGroq
from edgenia.ml.preprocessor import DataPreprocessor

from dotenv import load_dotenv
load_dotenv()

class CustomerSegmenter:
    """Segmentation dynamique intelligente"""
    
    def __init__(self, n_clusters: int = 4):
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.preprocessor = DataPreprocessor()
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
        self.is_fitted = False
    
    def segment(self, df: pd.DataFrame) -> Dict:
        """Segmente les clients et donne des noms intelligents"""
        X = self.preprocessor.preprocess(df)
        clusters = self.model.fit_predict(X)
        
        df = df.copy()
        df['segment_id'] = clusters
        
        self.is_fitted = True
        
        # Description des segments
        numeric_cols = df.select_dtypes(include=['number']).columns
        summary = df.groupby('segment_id')[numeric_cols].mean().to_dict()
        
        # Noms intelligents des segments par LLM
        segment_names = self._name_segments(df, summary)
        
        return {
            "segments": df['segment_id'].value_counts().to_dict(),
            "segment_names": segment_names,
            "summary": summary,
            "cluster_labels": clusters.tolist()
        }
    
    def _name_segments(self, df: pd.DataFrame, summary: Dict) -> Dict[int, str]:
        """Le LLM donne des noms intelligents aux segments"""
        prompt = f"""
Analyse ces statistiques de segments clients :

{summary}

Donne un nom court et professionnel à chaque segment (ex: "Clients VIP", "Clients Inactifs", "Nouveaux Clients", etc.).
Retourne uniquement un JSON : {{"0": "Nom du segment 0", "1": "Nom du segment 1", ...}}
"""
        try:
            response = self.llm.invoke(prompt)
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                return eval(json_match.group(0))
        except:
            pass
        
        # Fallback
        return {i: f"Segment {i}" for i in range(len(summary))}