import pandas as pd
from typing import Dict, Any
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from langchain_groq import ChatGroq
from edgenia.ml.preprocessor import DataPreprocessor
from dotenv import load_dotenv

load_dotenv()

class CustomerSegmenter:
    """Segmentation dynamique intelligente"""
    
    def __init__(self, n_clusters: int = None, method: str = "kmeans"):
        self.method = method
        self.preprocessor = DataPreprocessor()
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
        self.is_fitted = False
        self.n_clusters = n_clusters
    
    def segment(self, df: pd.DataFrame) -> Dict:
        """Segmente les clients"""
        n_samples = len(df)
        n_clusters = self.n_clusters or min(4, max(2, n_samples - 1))
        n_clusters = min(n_clusters, n_samples)
        n_clusters = max(1, n_clusters)
        
        if self.method == "hierarchical":
            self.model = AgglomerativeClustering(n_clusters=n_clusters)
        else:
            self.model = KMeans(n_clusters=n_clusters, random_state=42)
        
        X = self.preprocessor.preprocess(df)
        clusters = self.model.fit_predict(X)
        
        df = df.copy()
        df['segment_id'] = clusters
        
        self.is_fitted = True
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        summary = df.groupby('segment_id')[numeric_cols].mean().to_dict()
        
        segment_names = self._name_segments(df, summary)
        
        return {
            "segments": df['segment_id'].value_counts().to_dict(),
            "segment_names": segment_names,
            "summary": summary,
            "method": self.method,
            "n_clusters": n_clusters
        }
    
    def _name_segments(self, df: pd.DataFrame, summary: Dict) -> Dict[int, str]:
        prompt = f"""
Analyse ces statistiques de segments clients :

{summary}

Donne un nom court et professionnel à chaque segment.
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
        return {i: f"Segment {i}" for i in range(len(summary))}