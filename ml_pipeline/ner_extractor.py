import spacy
import re
import sys
from typing import List, Dict, Any

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
            # Add site-packages to path so it can be found immediately if needed
            import site
            import importlib
            importlib.invalidate_caches()
            _nlp = spacy.load("en_core_web_sm")
    return _nlp

# A simple list of skills to match against (in a real scenario, this would be an exhaustive DB or loaded from a file)
COMMON_SKILLS = set([
    'python', 'java', 'c++', 'javascript', 'react', 'angular', 'vue', 'django', 'flask',
    'spring', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'machine learning',
    'deep learning', 'nlp', 'computer vision', 'docker', 'kubernetes', 'aws', 'gcp', 'azure',
    'html', 'css', 'git', 'linux', 'agile', 'scrum', 'data analysis', 'pandas', 'numpy',
    'scikit-learn', 'tensorflow', 'pytorch', 'spacy', 'nltk', 'excel', 'tableau', 'power bi'
])

def extract_skills(text: str) -> List[str]:
    """Extract skills from text using spaCy and keyword matching."""
    nlp = get_nlp()
    doc = nlp(text.lower())
    extracted = set()
    
    # Simple keyword matching
    for token in doc:
        if token.text in COMMON_SKILLS:
            extracted.add(token.text)
            
    # Also check multi-word skills
    text_lower = text.lower()
    for skill in COMMON_SKILLS:
        if " " in skill and skill in text_lower:
            extracted.add(skill)
            
    return list(extracted)

def extract_experience(text: str) -> float:
    """Extract years of experience from text."""
    # Look for patterns like "5 years of experience", "3+ years", "10 yrs"
    pattern = r'(\d+)(?:\+)?\s*(?:years?|yrs?)\s*(?:of)?\s*experience'
    matches = re.findall(pattern, text.lower())
    
    if matches:
        try:
            # Take the max if multiple are found
            years = max([float(m) for m in matches])
            return years
        except ValueError:
            pass
            
    return 0.0

def extract_education(text: str) -> str:
    """Extract highest education level."""
    text_lower = text.lower()
    if 'phd' in text_lower or 'ph.d' in text_lower or 'doctorate' in text_lower:
        return 'PhD'
    elif 'master' in text_lower or 'm.s' in text_lower or 'ma' in text_lower or 'mba' in text_lower:
        return 'Master'
    elif 'bachelor' in text_lower or 'b.s' in text_lower or 'ba' in text_lower or 'bsc' in text_lower:
        return 'Bachelor'
    elif 'associate' in text_lower:
        return 'Associate'
    return 'Not Specified'

def extract_entities(text: str) -> Dict[str, Any]:
    """Extract all relevant entities from resume text."""
    return {
        'skills': extract_skills(text),
        'years_of_experience': extract_experience(text),
        'education_level': extract_education(text)
    }
