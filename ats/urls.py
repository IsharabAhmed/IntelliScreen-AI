from django.urls import path
from . import views

app_name = 'ats'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_resumes, name='upload_resumes'),
    path('jd/create/', views.create_jd, name='create_jd'),
    path('jd/<int:jd_id>/', views.jd_detail, name='jd_detail'),
    path('candidate/<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),
    path('api/rankings/<int:jd_id>/', views.api_get_rankings, name='api_get_rankings'),
    path('api/stats/', views.api_get_stats, name='api_get_stats'),
]
