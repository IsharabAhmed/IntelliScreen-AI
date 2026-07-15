import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_screener.settings')
django.setup()

from ats.models import JobDescription
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

if not user:
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

jd, created = JobDescription.objects.get_or_create(
    title="Python/Django Developer",
    defaults={
        "description": "We are looking for a Python/Django Developer with strong skills in Python, Django, and REST APIs.",
        "extracted_skills": ["python", "django", "rest"],
        "user": user,
    }
)

if not created:
    jd.extracted_skills = ["python", "django", "rest"]
    jd.description = "We are looking for a Python/Django Developer with strong skills in Python, Django, and REST APIs."
    jd.save()

print("Job Description created successfully.")
