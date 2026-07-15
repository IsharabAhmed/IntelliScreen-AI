import hashlib
from celery import shared_task
from django.core.files.storage import default_storage
from .models import Candidate, Resume
from ml_pipeline.parser import parse_resume
from ml_pipeline.ner_extractor import extract_entities

@shared_task
def process_resume(file_path, original_name):
    """
    Background task to parse and extract information from an uploaded resume.
    """
    try:
        # Open file from storage
        with default_storage.open(file_path, 'rb') as f:
            file_content = f.read()
            
            # Generate hash to prevent duplicate processing
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            if Resume.objects.filter(file_hash=file_hash).exists():
                return f"Duplicate resume detected: {original_name}"
                
            # Parse text
            f.seek(0)
            text = parse_resume(f, original_name)
            
            # Extract entities
            entities = extract_entities(text)
            
            # Extract basic info (mocked here, ideally SpaCy NER for ORG/PERSON would get this)
            # For this MVP, we use the filename as the candidate name if not clearly extractable
            name = original_name.rsplit('.', 1)[0].replace('_', ' ').title()
            
            # Create Candidate
            candidate, created = Candidate.objects.get_or_create(
                name=name,
                defaults={'email': f"{name.replace(' ', '.').lower()}@example.com"} # Mock email
            )
            
            # Create Resume record
            Resume.objects.create(
                candidate=candidate,
                file=file_path, # Path in storage
                parsed_text=text,
                extracted_skills=entities.get('skills', []),
                education_level=entities.get('education_level', ''),
                years_of_experience=entities.get('years_of_experience', 0.0),
                file_hash=file_hash
            )
            
            return f"Successfully processed {original_name}"
            
    except Exception as e:
        return f"Error processing {original_name}: {str(e)}"
