from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from typing import List, Dict, Any
import pandas as pd

def cluster_resumes(resumes: List[Dict[str, Any]], num_clusters: int = 5) -> Dict[int, List[int]]:
    """
    Groups resumes into clusters based on text content to identify candidate cohorts.
    resumes: [{'id': int, 'text': str}, ...]
    Returns a dict mapping cluster_id to a list of candidate_ids.
    """
    if not resumes or len(resumes) < num_clusters:
        # Not enough data to cluster meaningfully
        return {0: [r['id'] for r in resumes]}
        
    texts = [r['text'] for r in resumes]
    ids = [r['id'] for r in resumes]
    
    # Vectorize
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Cluster
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(tfidf_matrix)
    
    # Assign clusters
    clusters = {}
    for i, cluster_id in enumerate(kmeans.labels_):
        cluster_id = int(cluster_id)
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(ids[i])
        
    return clusters
