from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Skill
from .models import Profile

@login_required
def profile_view(request):
    profile = request.user.profile
    skills = Skill.objects.all()

    if request.method == 'POST':
        selected_skills = request.POST.getlist('skills')
        experience = request.POST.get('experience')
        profile.matching_mode = request.POST.get('matching_mode','skills')
        profile.skills.set(request.POST.getlist('skills'))
        # profile.skills.set(selected_skills)
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
        profile.save()
        print("MATCHING MODE:", profile.matching_mode)
        profile.experience = int(experience)
        profile.save()

        return redirect('dashboard')

    return render(request, 'accounts/profile.html', {
        'skills': skills,
        'profile': profile, 
        'user_skills': profile.skills.all(),
        'experience': profile.experience
        
    })
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # auto login after signup
            return redirect('profile')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')
