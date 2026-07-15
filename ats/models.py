from django.db import models
from django.conf import settings

class JobDescription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    extracted_skills = models.JSONField(default=list, blank=True)
    extracted_experience = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    parsed_text = models.TextField(blank=True)
    extracted_skills = models.JSONField(default=list, blank=True)
    education_level = models.CharField(max_length=100, blank=True)
    years_of_experience = models.FloatField(default=0.0)
    file_hash = models.CharField(max_length=64, unique=True, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Resume for {self.candidate.name}"

class Ranking(models.Model):
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name='rankings')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='rankings')
    score = models.FloatField()
    skill_match_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job_description', 'candidate')
        indexes = [
            models.Index(fields=['job_description', '-score']),
        ]

    def __str__(self):
        return f"{self.candidate.name} - {self.score}% for {self.job_description.title}"
