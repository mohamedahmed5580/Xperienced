import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from . import models
from .models import User, Token, Request, Offer, Notification, Category, Message
from .emails import EmailSender

emailSender = EmailSender(
    "myspaceduckbot@gmail.com",
    "nrsw vzer tbkl jzuw",
)

# Create your views here.

def checkRequest(request, auth=True, post=True):
    if post and request.method != "POST":
        return JsonResponse({"error": "Only post method is allowed."}, status=400)
    if auth and not request.user.is_authenticated():
        return JsonResponse({"error": "Authentication error."}, status=401)
    return None

def checkFormErrors(form):
    errors = []
    for field in form:
        errors += list(field.errors)
    return errors

def checkKeys(dic, keys):
    for key in keys:
        if dic.get(key) is None:
            return key

def index(request):
    return render(request, 'assistantFinder/index.html')

def login_view(request):
    return render(request, 'assistantFinder/login.html')

def signup_view(request):
    return render(request, 'assistantFinder/signup.html')

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))

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
    response = checkRequest(request, auth=False)
    if response is not None:
        return response
    data = json.loads(request.body)
    missingKey = checkKeys(data, NewUserForm.Meta.fields)
    if missingKey is not None:
        return JsonResponse({"error": f"Missing {missingKey}."}, status=400)

    if data["password"] != data["confirmation"]:
        return JsonResponse({"error": "Passwords don't match."}, status=400)

    userForm = NewUserForm(data)
    if not userForm.is_valid():
        errors = checkFormErrors(userForm)
        return JsonResponse({"error": errors[0]}, status=400)

    if models.User.objects.filter(username=data["username"]).exists():
        return JsonResponse({"error": "Username already taken."}, status=400)
    user = userForm.save(commit=False)
    user.set_password(userForm.cleaned_data["password"])
    user.save()
    auth.login(request, user)
    return JsonResponse({"success": "User authenticated successfully"}, status=200)

def login(request):
    response = checkRequest(request, auth=False)
    if response is not None:
        return response
    data = json.loads(request.body)
    missingKey = checkKeys(data, ["username", "password"])
    if missingKey is not None:
        return JsonResponse({"error": f"Missing {missingKey}."}, status=400)
    username = data["username"]
    password = data["password"]
    user = auth.authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid username and/or password."}, status=401)
    auth.login(request, user)
    return JsonResponse({"success": "User authenticated successfully"}, status=200)

def send_email_token(request):
    response = checkRequest(request)
    if response is not None:
        return response
    try:
        key = request.user.createToken()
        emailSender.sendPlain(request.user.email, "Xperienced: Email Verification", f"Your email verification token: {key}")
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
        return JsonResponse({"error": "You have to request a token first."}, status=400) 
    if token.key != data["token"]:
        return JsonResponse({"error": "Invalid token."}, status=400) 
    if token.isExpired():
        return JsonResponse({"error": "Token is expired."}, status=400) 
    request.user.verifyEmail()
    return JsonResponse({"success": "Email verified Successfully."}, status=200) 

def new_request_view(request):
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

def new_request(request):
    response = checkRequest(request)
    if response is not None:
        return response
    data = json.loads(request.body)
    if not data.get("request"):
        return JsonResponse({"error": "Missing request."}, status=400)
    missingKey = checkKeys(data["request"], NewRequestForm.Meta.fields)
    if missingKey is not None:
        return JsonResponse({"error": f"Missing {missingKey}."}, status=400)
    requestForm = NewRequestForm(data)
    
    if not requestForm.is_valid():
        errors = checkFormErrors(requestForm)
        return JsonResponse({"error": errors[0]}, status=400)
    request = requestForm.save(commit=False)
    request.owner = request.user
    request.save()
    return JsonResponse({"success": request.id}, status=200)

def requests_view(request):
    return render(request, 'assistantFinder/offer_help.html', {
        "categories": Category.objects.all()
    })

def requests(request):
    data = json.loads(request.body)
    requests = []
    for req in Request.objects.all():
        if req.state() == models.OPEN:
            requests.append(req)
    if data.get("category"):
        if Category.objects.filter(name=data["category"]) is None:
            return JsonResponse({"error": "Specified category doesn't exist"}, status=400)
        requests.filter(category=data["category"])
    return JsonResponse({"requests": requests}, status=200)


def request_view(request, id):
    return render(request, 'assistantFinder/add_offer.html', {
        "request": Request.objects.get(id=id)
    })

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
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400) 
    requestInstance = Request.objects.get(id=id)
    data = json.loads(request.body)
    if requestInstance.owner == request.user:
        return JsonResponse({"error": "You can't add an offer to a request that you made."}, status=400)
    if requestInstance.offers.filter(bidder=request.user):
        return JsonResponse({"error": "You already made an offer to that request"}, status=400)
    if not data.get("offer"):
        return JsonResponse({"error": "Missing offer."}, status=400)
    missingKey = checkKeys(data["offer"], NewOfferForm.Meta.fields)
    if missingKey is not None:
        return JsonResponse({"error": f"Missing {missingKey}."}, status=400)
    
    offerForm = NewOfferForm(data["offer"])
    offer = offerForm.save(commit=False)
    offer.bidder = request.user
    offer.request = requestInstance
    offer.save()
    return JsonResponse({"success": "Offer added successfully."}, status=200)

def profile(request, username):
    return render(request, 'assistantFinder/profile.html', {
        "profile": User.objects.get(username=username)
    })

def temp_profile(request):
    return render(request, 'assistantFinder/profile.html') 

def balance_view(request):
    return render(request, 'assistantFinder/account_balance.html')
    
def notifications_view(request):
    return render(request, "assistantFinder/Notifications.html")

def messages_view(request):
    return render(request, "assistantFinder/Messages.html")

def notifications(request):
    response = checkRequest(request, post=False)
    if response is not None:
        return response
    return JsonResponse({"notifications": Notification.objects.filter(user=request.user)}, status=200)

def messages(request):
    response = checkRequest(request, post=False)
    if response is not None:
        return response
    messages = []
    for room in request.user.student_chatrooms + request.user.mentor_chatrooms:
        messages += room.messages.exclude(sender=request.user)
    messages = messages.order_by("-timestamp")
    return JsonResponse({"messages": messages}, status=200)