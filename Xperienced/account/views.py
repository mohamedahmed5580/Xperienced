from django.shortcuts import render, redirect
from .forms import LoginForm,SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
# Create your views here.
from django.contrib import messages
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import  logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Skill
def index(request):
    return render(request, 'pages/index.html')

def register(request):
    return render(request,'pages\signup.html')

def logout_view(request):
    auth_logout(request)
    return redirect('index') 
    
@login_required
def signup_view(request):
    print(request.POST)
    if request.method == 'POST':
        form = SignUpForm(request.POST) 
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('login_view')
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = SignUpForm() 
    return render(request, 'signup.html', {'form': form})

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
    if request.method == 'POST':
        skill_name = request.POST.get('skill-input')
        user_id = request.user.id
        
        if skill_name and user_id:
            user = User.objects.get(id=user_id)
            skill = Skill(user=user, skill=skill_name)
            skill.save()
            user_skills = Skill.objects.filter(user=request.user)
            skills = [skill.skill for skill in user_skills]
            
            return JsonResponse({'status': 'success', 'skills': skills})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    
    user_skills = Skill.objects.filter(user=request.user)
    skills = [skill.skill for skill in user_skills]

    return render(request, 'pages/profile.html', {'skills': skills})
def admin(request):
    print('in admin')
    return render(request,'pages\index.html')

def user(request):
    print('in user')
    return render(request,'pages\profileu.html')

def login_views (request):
    return render(request, 'pages/index.html')

def profile_view (request):
    
    return render(request, 'pages/profile.html', {'skills': skills})
