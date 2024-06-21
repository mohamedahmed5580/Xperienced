from django.shortcuts import render, redirect
from .forms import LoginForm,SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
import json
from django.middleware.csrf import get_token
# Create your views here.
from django.contrib import messages
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import  logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Skill
from .forms import EditProfileForm,EditAboutForm,EditImageProfileForm
def index(request):
    return render(request, 'pages/index.html')

def register(request):
    return render(request,'pages\signup.html')
def profile(request):
    return render(request,'pages\profile.html')

def logout_view(request):
    auth_logout(request)
    return redirect('index') 

@csrf_exempt
def signup(request):
    print(request.POST)
    if request.method == 'POST':
        form = SignUpForm(request.POST) 
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("User authenticated and logged in")
                return redirect('index')  # Ensure this matches the name in your urls.py
            else:
                print("User authentication failed")
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = SignUpForm() 
    return render(request, 'pages/signup.html', {'form': form})

@csrf_exempt
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    # print(form)
    print(request.POST) 
    if request.method == 'POST':
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')   
            user = authenticate(username=username, password=password)

            print(user)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                msg = 'error'
        else:
            msg = 'error'
    
    return render(request, 'pages/login.html', {'form': form, 'msg': msg})

@login_required
def skills(request):
    user = request.user
    if request.method == 'POST':
        skill_name = request.POST.get('skill-input')
        if skill_name:
            Skill.objects.create(user=user, skill=skill_name)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)
    
    user_skills = Skill.objects.filter(user=user)
    skills = [skill.skill for skill in user_skills]
    return JsonResponse({'status': 'success', 'skills': skills})

@login_required
def delete_skill(request, skill_id):
    if request.method == 'POST':
        try:
            skill = Skill.objects.get(id=skill_id, user=request.user)
            skill.delete()
            messages.success(request, "Skill successfully deleted.")
        except Skill.DoesNotExist:
            messages.error(request, "Skill not found.")
        return redirect('profile', id=request.user.id)
    return redirect('profile', id=request.user.id)

def login_views (request):
    return render(request, 'pages/login.html')

def profile_view(request,id):
    if not User.objects.filter(id=id).exists():
        return JsonResponse({"error": "Profile doesn't exist."}, status=400) 
    user = User.objects.get(id=id)
    profile = {
        "id":user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone":user.phone,
        "password":user.password,
        "description":user.description,
        "image":user.image,
    }
    print(profile)
    user_skills = Skill.objects.filter(user=user)
    return render(request, 'pages/profile.html', {
        "profile": profile,
        "skills": user_skills,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        print(request.POST)
        print(form.is_valid)
        if form.is_valid():
            form.save()
            print('form is saved')
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('index')  # Replace 'profile' with your profile view name
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'pages/profile.html', {'form': form})


@login_required
@csrf_exempt
def edit_about(request):
    if request.method == 'POST':
        form = EditAboutForm(request.POST, instance=request.user)
        print(request.POST)
        print(form.is_valid)
        if form.is_valid():
            form.save()
            print('form is saved')
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('index')  # Replace 'profile' with your profile view name
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditAboutForm(instance=request.user)
    
    return render(request, 'pages/profile.html', {'form': form})

    
@login_required
def edit_image_profile(request):
    if request.method == 'POST':
        form = EditImageProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})