import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from .models import User, Token
from .emails import EmailSender
from random import randint

emailSender = EmailSender(
    "myspaceduckbot@gmail.com",
    "nrsw vzer tbkl jzuw",
)

# Create your views here.

def index(request):
    return render(request, 'assistantFinder/index.html')

def login_view(request):
    return render(request, 'assistantFinder/login.html')

def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only post method is allowed."}, status=400)
    data = json.loads(request.body)
    if not data.get("username"):
        return JsonResponse({"error": "Missing username."}, status=400)
    if not data.get("password"):
        return JsonResponse({"error": "Missing password."}, status=400)
    username = data["username"]
    password = data["password"]
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid username and/or password."}, status=401)
    login(request, user)
    return JsonResponse({"success": "User authenticated successfully"}, status=200)

def signup_view(request):
    return render(request, 'assistantFinder/signup.html')

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "password"
        )

def signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only post method is allowed."}, status=400)
    data = json.loads(request.body)
    for key in ["first_name", "last_name", "username", "email", "phone", "password", "confirmation"]:
        if not data.get(key):
            return JsonResponse({"error": f"Missing {key}."}, status=400)

    if data["password"] != data["confirmation"]:
        return JsonResponse({"error": "Passwords don't match."}, status=400)

    userForm = NewUserForm(data)
    if not userForm.is_valid():
        errors = []
        for field in recipeForm:
            errors += field.errors()
        return JsonResponse({"error": errors[0]}, status=400)

    if User.objects.exists(username=data["username"]):
        return JsonResponse({"error": "Username already taken."}, status=400)
    user = userForm.save()
    login(request, user)
    return JsonResponse({"success": "User authenticated successfully"}, status=200)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def send_email_token(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only post method is allowed."}, status=400)
    try:
        key = request.user.createToken()
        emailSender.sendPlain(request.user.email, f"Your email verification token: {key}")
    except Exception:
        return JsonResponse({"error": "Something went wrong"}, status=500)
    return JsonResponse({"success": "Token sent successfully"}, status=200) 

@login_required(login_url='login')
def verify_email(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only post method is allowed."}, status=400)

    data = json.loads(request.body)
    if not data.get("token"):
        return JsonResponse({"error": "Missing verification token."}, status=400) 
    token = request.user.getToken()
    if token is None:
        return JsonResponse({"error": "You have to request a new token first."}, status=400) 
    if token.key != data["token"]:
        return JsonResponse({"error": "Invalid token."}, status=400) 
    if token.isExpired():
        return JsonResponse({"error": "Token is expired."}, status=400) 
    request.user.verifyEmail()
    return JsonResponse({"success": "Email verified Successfully."}, status=200) 

@login_required(login_url='login')
def find_assistant(request):
    return render(request, 'assistantFinder/find_assistant.html')

@login_required(login_url='login')
def offer_help(request):
    return render(request, 'assistantFinder/offer_help.html')

def profile(request):
    return render(request, 'assistantFinder/profile.html')

def add_offer(request):
    return render(request, 'assistantFinder/add_offer.html')

def account_balance(request):
    return render(request, 'assistantFinder/account_balance.html')