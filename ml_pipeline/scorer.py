import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

def calculate_similarity(jd_text: str, resume_texts: List[str]) -> List[float]:
    """
    Calculate TF-IDF cosine similarity between a Job Description and multiple resumes.
    Returns a list of scores (0.0 to 1.0) corresponding to the resume_texts order.
    """
    if not jd_text or not resume_texts:
        return []
        
    documents = [jd_text] + resume_texts
    
    # Initialize TF-IDF Vectorizer
    # stop_words='english' removes common English words (the, a, is, etc.)
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity of the JD (index 0) against all resumes (index 1 to end)
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        return cosine_similarities.tolist()
    except ValueError:
        # Occurs if documents only contain stop words or are completely empty after preprocessing
        return [0.0] * len(resume_texts)

def score_candidates(jd_data: Dict[str, Any], resumes_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scores a list of candidates against a JD based on text similarity and skill match.
    jd_data: {'text': str, 'skills': list}
    resumes_data: [{'id': int, 'text': str, 'skills': list}]
    
    Returns a list of dicts with 'id', 'score' (0-100), and 'skill_match_details'.
    """
    jd_text = jd_data.get('text', '')
    jd_skills = set(s.lower() for s in jd_data.get('skills', []))
    
    resume_texts = [r.get('text', '') for r in resumes_data]
    
    # 1. Text Similarity Score (TF-IDF Cosine Similarity)
    similarity_scores = calculate_similarity(jd_text, resume_texts)
    
    results = []
    
    for i, resume in enumerate(resumes_data):
        resume_skills = set(s.lower() for s in resume.get('skills', []))
        
        # 2. Skill Match Score
        if jd_skills:
            matched_skills = jd_skills.intersection(resume_skills)
            missing_skills = jd_skills.difference(resume_skills)
            skill_score = len(matched_skills) / len(jd_skills)
        else:
            matched_skills = set()
            missing_skills = set()
            skill_score = 0.0 if not resume_skills else 0.5 # Neutral if no JD skills defined
            
        # 3. Weighted Final Score (e.g., 60% text similarity, 40% exact skill match)
        text_score = similarity_scores[i]
        final_score = (text_score * 0.6) + (skill_score * 0.4)
        
        # Convert to percentage (0-100)
        final_score_pct = round(final_score * 100, 2)
        
        results.append({
            'candidate_id': resume.get('id'),
            'score': final_score_pct,
            'skill_match_details': {
                'matched': list(matched_skills),
                'missing': list(missing_skills),
                'candidate_skills': list(resume_skills)
            }
        })
        
    # Sort descending by score
    results.sort(key=lambda x: x['score'], reverse=True)
    return results
