from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django.db import models

from .models import Job
from accounts.models import Profile
from .ats_utils import extract_resume_text, calculate_ats_score

def home_view(request):
    return render(request, 'jobs/home.html')


@login_required
def explore_view(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/explore.html', {
        'jobs': jobs
    })
@login_required
def dashboard_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    mode = request.GET.get('mode')
    if mode not in ['skills', 'resume']:
        mode = 'skills'   # default

    # -------------------------------
    # MODE 1: SKILL-BASED MATCHING
    # -------------------------------
    if mode == 'skills':
        user_skills = profile.skills.all()
        user_experience = profile.experience

        jobs = Job.objects.annotate(
            total_required=Count('required_skills', distinct=True),
            matched_skills=Count(
                'required_skills',
                filter=models.Q(required_skills__in=user_skills),
                distinct=True
            )
        ).filter(
            matched_skills__gt=0,
            # matched_skills=models.F('total_required'), for all skill compulsary
            min_experience__lte=user_experience
        ).order_by('-matched_skills')

        return render(request, 'jobs/dashboard.html', {
    'jobs': jobs,
    'user_skills': user_skills,
    'user_skill_ids': list(user_skills.values_list('id', flat=True)),
    'mode': 'skills'
})

    # -------------------------------
    # MODE 2: RESUME (ATS) MATCHING
    # -------------------------------
    if mode == 'resume':
        matched_jobs = []

        if profile.resume:
            resume_text = extract_resume_text(profile.resume.path)

            for job in Job.objects.all():
                ats_score = calculate_ats_score(resume_text, job)

                if ats_score >= 80:
                    job.ats_score = ats_score  # dynamic attribute
                    matched_jobs.append(job)

        return render(request, 'jobs/dashboard.html', {
            'jobs': matched_jobs,
            'mode': 'resume'
        })

    # -------------------------------
    # FALLBACK
    # -------------------------------
    return render(request, 'jobs/dashboard.html', {
        'jobs': jobs,
        'mode': mode
    })
