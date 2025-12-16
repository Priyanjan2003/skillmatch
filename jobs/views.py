from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from .models import Job
from django.db import models

@login_required
def dashboard_view(request):
    profile = request.user.profile
    user_skills = profile.skills.all()

    # Count how many skills each job requires
    jobs = Job.objects.annotate(
        total_required=Count('required_skills', distinct=True),
        matched_skills=Count(
            'required_skills',
            filter=models.Q(required_skills__in=user_skills),
            distinct=True
        )
    ).filter(total_required=models.F('matched_skills'))

    return render(request, 'jobs/dashboard.html', {'jobs': jobs})
