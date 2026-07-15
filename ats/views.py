from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .models import JobDescription, Candidate, Resume, Ranking
from .tasks import process_resume
from ml_pipeline.scorer import score_candidates
from ml_pipeline.ner_extractor import extract_skills, extract_experience

@login_required
def dashboard(request):
    jds = JobDescription.objects.filter(user=request.user).order_by('-created_at')
    total_resumes = Resume.objects.count()
    return render(request, 'ats/dashboard.html', {
        'jds': jds,
        'total_resumes': total_resumes
    })

@login_required
def upload_resumes(request):
    if request.method == 'POST':
        files = request.FILES.getlist('resumes')
        for f in files:
            # Save file temporarily
            file_name = default_storage.save(f'uploads/{f.name}', f)
            # Dispatch Celery task
            process_resume.delay(file_name, f.name)
            
        return redirect('ats:dashboard')
        
    return render(request, 'ats/upload.html')

@login_required
def create_jd(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Extract skills and experience from JD
        skills = extract_skills(description)
        exp = extract_experience(description)
        
        jd = JobDescription.objects.create(
            title=title,
            description=description,
            extracted_skills=skills,
            extracted_experience=exp,
            user=request.user
        )
        return redirect('ats:jd_detail', jd_id=jd.id)
        
    return render(request, 'ats/create_jd.html')

@login_required
def jd_detail(request, jd_id):
    jd = get_object_or_404(JobDescription, id=jd_id, user=request.user)
    
    # Calculate rankings on the fly (or fetch from DB if cached/pre-calculated)
    # For this implementation, we calculate on the fly for sub-second responses since TF-IDF is fast
    # and we only have parsed text.
    resumes = Resume.objects.select_related('candidate').all()
    
    resumes_data = []
    for r in resumes:
        resumes_data.append({
            'id': r.candidate.id,
            'text': r.parsed_text,
            'skills': r.extracted_skills
        })
        
    jd_data = {
        'text': jd.description,
        'skills': jd.extracted_skills
    }
    
    # Run scorer
    if resumes_data:
        ranked_results = score_candidates(jd_data, resumes_data)
        
        # Update or create Ranking records
        for res in ranked_results:
            Ranking.objects.update_or_create(
                job_description=jd,
                candidate_id=res['candidate_id'],
                defaults={
                    'score': res['score'],
                    'skill_match_details': res['skill_match_details']
                }
            )
            
    rankings = Ranking.objects.filter(job_description=jd).select_related('candidate').order_by('-score')
    
    return render(request, 'ats/jd_detail.html', {
        'jd': jd,
        'rankings': rankings
    })

@login_required
def candidate_detail(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    resumes = candidate.resumes.all()
    rankings = candidate.rankings.select_related('job_description').all()
    
    return render(request, 'ats/candidate_detail.html', {
        'candidate': candidate,
        'resumes': resumes,
        'rankings': rankings
    })

# --- API Endpoints for Chart.js ---
@login_required
def api_get_stats(request):
    # Aggregated stats for the dashboard charts
    resumes = Resume.objects.all()
    
    # Education distribution
    edu_dist = {}
    # Experience distribution
    exp_dist = {'0-2': 0, '3-5': 0, '6-10': 0, '10+': 0}
    # Skill frequencies
    skill_freq = {}
    
    for r in resumes:
        edu = r.education_level or 'Not Specified'
        edu_dist[edu] = edu_dist.get(edu, 0) + 1
        
        exp = r.years_of_experience
        if exp <= 2: exp_dist['0-2'] += 1
        elif exp <= 5: exp_dist['3-5'] += 1
        elif exp <= 10: exp_dist['6-10'] += 1
        else: exp_dist['10+'] += 1
            
        for skill in r.extracted_skills:
            skill = skill.lower()
            skill_freq[skill] = skill_freq.get(skill, 0) + 1
            
    # Top 10 skills
    top_skills = sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return JsonResponse({
        'education': edu_dist,
        'experience': exp_dist,
        'skills': dict(top_skills)
    })

@login_required
def api_get_rankings(request, jd_id):
    jd = get_object_or_404(JobDescription, id=jd_id, user=request.user)
    rankings = Ranking.objects.filter(job_description=jd).select_related('candidate').order_by('-score')
    
    data = []
    for r in rankings:
        data.append({
            'candidate_name': r.candidate.name,
            'score': r.score,
            'matched_skills': r.skill_match_details.get('matched', []),
            'missing_skills': r.skill_match_details.get('missing', [])
        })
    return JsonResponse({'rankings': data})
