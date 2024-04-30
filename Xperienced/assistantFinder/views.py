import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from .models import User, Token, Request, Offer
from .emails import EmailSender
from random import randint

emailSender = EmailSender(
    "myspaceduckbot@gmail.com",
    "nrsw vzer tbkl jzuw",
)

# Create your views here.

def checkRequest(request, auth=True):
    if request.method != "POST":
        return JsonResponse({"error": "Only post method is allowed."}, status=400)
    if not request.user.is_authenticated():
        return JsonResponse({"error": "Authentication error."}, status=401)
    return None

def checkFormErrors(form):
    errors = []
    for field in form:
        errors += field.errors()
    return errros

def index(request):
    return render(request, 'assistantFinder/index.html')

def login_view(request):
    return render(request, 'assistantFinder/login.html')

def login(request):
    response = checkRequest(request, False)
    if response is not None:
        return response
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
    response = checkRequest(request, False)
    if response is not None:
        return response
    data = json.loads(request.body)
    for key in ["first_name", "last_name", "username", "email", "phone", "password", "confirmation"]:
        if not data.get(key):
            return JsonResponse({"error": f"Missing {key}."}, status=400)

    if data["password"] != data["confirmation"]:
        return JsonResponse({"error": "Passwords don't match."}, status=400)

    userForm = NewUserForm(data)
    if not userForm.is_valid():
        errors = checkFormErrors(userForm)
        return JsonResponse({"error": errors[0]}, status=400)

    if User.objects.exists(username=data["username"]):
        return JsonResponse({"error": "Username already taken."}, status=400)
    user = userForm.save()
    login(request, user)
    return JsonResponse({"success": "User authenticated successfully"}, status=200)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def send_email_token(request):
    response = checkRequest(request)
    if response is not None:
        return response
    try:
        key = request.user.createToken()
        emailSender.sendPlain(request.user.email, f"Your email verification token: {key}")
    except Exception:
        return JsonResponse({"error": "Something went wrong"}, status=500)
    return JsonResponse({"success": "Token sent successfully"}, status=200) 

def verify_email(request):
    response = checkRequest(request)
    if response is not None:
        return response

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


def find_assistant_view(request):
    return render(request, 'assistantFinder/find_assistant.html')

class NewRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            "title",
            "description",
            "category",
            "budget",
        )

def find_assistant(request):
    response = checkRequest(request)
    if response is not None:
        return response
    data = json.loads(request.body)
    if not data.get("request"):
        return JsonResponse({"error": "Missing request."}, status=400)
    for key in ["title", "description", "category", "budegt"]:
        if not data["request"].get(key):
            return JsonResponse({"error": f"Missing {key}."}, status=400)
    requestForm = NewRequestForm(data)
    if not requestForm.is_valid():
        errors = checkFormErrors(requestForm)
        return JsonResponse({"error": errors[0]}, status=400)
    request = requestForm.save(commit=False)
    request.owner = request.user
    request.save()
    return JsonResponse({"success": request.id}, status=200)
    


def requests_view(request):
    return render(request, 'assistantFinder/offer_help.html')

def request_view(request):
    return render(request, 'assistantFinder/add_offer.html')


class NewOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = (
            "bid",
            "notes"
        )

def add_offer(request, id):
    response = checkRequest(request)
    if response is not None:
        return response
    data = json.loads(request.body)
    if not data.get("offer"):
        return JsonResponse({"error": "Missing request."}, status=400)
    for key in ["bid", "notes"]:
        if not data["offer"].get(key):
            return JsonResponse({"error": f"Missing {key}."}, status=400)
    offerForm = NewOfferForm(data["offer"])
    offer = offerForm.save(commit=False)
    offer.bidder = request.user
    offer.save()
    return JsonResponse({"success": request.id}, status=200) 

    
def profile(request):
    return render(request, 'assistantFinder/profile.html')

def account_balance(request):
    return render(request, 'assistantFinder/account_balance.html')

def notification(requst):
    return render(requst,'assistantFinder/Notifications.html')

def massages(requst):
    return render(requst,'assistantFinder/Messages.html')
def offer_help(requst):
    return render(requst,'assistantFinder/Offer_Help.html')

