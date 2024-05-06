import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from . import models
from django.core.paginator import Paginator
from .models import User, Token, Request, Offer, Notification, Category, Message, Connection, Skill
from .emails import EmailSender

emailSender = EmailSender(
    "myspaceduckbot@gmail.com",
    "nrsw vzer tbkl jzuw",
)

# Create your views here.

def inBounds(index, minIndex, maxIndex):
    return index >= minIndex and index <= maxIndex

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

def getPage(request, items, limit=20):
    if not len(items):
        return None
    items = items.order_by("-timestamp")
    pag = Paginator(items, limit)
    try:
        pageNum = int(request.GET["page"])
        assert pageNum <= pag.num_pages
    except Exception:
        pageNum = 1
    return pag.page(pageNum).object_list

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

def requests_view(request):
    return render(request, 'assistantFinder/offer_help.html', {
        "categories": Category.objects.all()
    })


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

def profile_view(request, username):
    return render(request, 'assistantFinder/profile.html', {
        "profile": User.objects.get(username=username)
    })

def balance_view(request):
    return render(request, 'assistantFinder/account_balance.html')
    
def notifications_view(request):
    return render(request, "assistantFinder/Notifications.html")

def messages_view(request):
    return render(request, "assistantFinder/Messages.html")

# API

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
    if request.user.verifiedEmail:
        return JsonResponse({"error": "Your email is already verified"}, status=403) 
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
    if request.user.verifiedEmail:
        return JsonResponse({"error": "Your email is alraedy verified"}, status=403) 
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

def categories(request):
    return JsonResponse({"categories": Category.objects.all()}, status=200)

def request(request, id):
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400)
    requestInstance = Request.objects.get(id=id)
    requestInstance.requestCategory = requestInstance.category.name
    requestInstance.currentState = requestInstance.state()
    return JsonResponse({"request": requestInstance}, status=200) 

def cancel_request(request, id):
    response = checkRequest(request)
    if response is not None:
        return response
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400)
    requestInstance = Request.objects.get(id=id)
    if requestInstance.owner != request.user:
        return JsonResponse({"error": "Authorization error"}, status=403)
    if requestInstance.state() not in [models.OPEN, models.PENDING]:
        return JsonResponse({"error": "Request is already closed"}, status=403)
    requestInstance.cancelRequest()
    return JsonResponse({"success": "Request cancelled successfully"}, status=200)

def offers(request, id):
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400) 
    requestInstance = Request.objects.get(id=id)
    return JsonResponse({"offers": requestInstance.offers.all()})

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
    if not offerForm.is_valid():
        errors = checkFormErrors(offerForm)
        return JsonResponse({"error": errors[0]}, status=400)
    offer = offerForm.save(commit=False)
    offer.bidder = request.user
    offer.request = requestInstance
    offer.save()
    return JsonResponse({"success": "Offer added successfully."}, status=200)

def offer(request, id, offer_id):
    response = checkRequest(request)
    if response is not None:
        return response
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400)
    requestInstance = Request.objects.get(id=id)
    if requestInstance.offers.filter(id=offer_id) is None:
        return JsonResponse({"error": "Offer doesn't exist"}, status=400)
    return JsonResponse({"offer": requestInstance.offers.get(id=offer_id)}, status=200)

def accept_offer(request, id, offer_id):
    response = checkRequest(request)
    if response is not None:
        return response
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400)
    requestInstance = Request.objects.get(id=id)
    if requestInstance.owner != request.user:
        return JsonResponse({"error": "Authorization error"}, status=403)
    if requestInstance.state() != models.OPEN:
        return JsonResponse({"error": "Request isn't open anymore"}, status=403)
    if requestInstance.offers.filter(id=offer_id) is None:
        return JsonResponse({"error": "Offer doesn't exist"}, status=400)
    offer = requestInstance.offers.get(id=offer_id)
    if offer.state != models.PENDING:
        return JsonResponse({"error": "Can't accept offer"}, status=403)
    requestInstance.acceptOffer(offer)
    return JsonResponse({"success": "Offer accepted successfully"}, status=200)

def cancel_offer(request, id, offer_id):
    response = checkRequest(request)
    if response is not None:
        return response
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400)
    requestInstance = Request.objects.get(id=id)

    if requestInstance.offers.filter(id=offer_id) is None:
        return JsonResponse({"error": "Offer doesn't exist"}, status=400)
    offer = requestInstance.offers.get(id=offer_id)
    if offer.bidder != request.user:
        return JsonResponse({"error": "Authorization error"}, status=403)
    if requestInstance.state() != models.OPEN:
        return JsonResponse({"error": "Request is no longer open"}, status=403)
    offer.state = models.CANCELLED
    return JsonResponse({"success": "Offer cancelled successfully"}, status=200)

def complete_request(request, id):
    response = checkRequest(request)
    if response is not None:
        return response
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400)
    requestInstance = Request.objects.get(id=id)
    if requestInstance.owner != request.user:
        return JsonResponse({"error": "Authorization error"}, status=403)
    if requestInstance.state() != models.PENDING:
        return JsonResponse({"error": "Can't complete a request without accepting an offer"}, status=403)
    requestInstance.completeRequest()
    return JsonResponse({"success": "Request completed successfully"}, status=200)

def chat_messages(request, id):
    response = checkRequest(request)
    if response is not None:
        return response
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400)
    requestInstance = Request.objects.get(id=id)
    if Connection.objects.filter(request=requestInstance) is None:
        return JsonResponse({"error": "Authorization error"}, status=403)
    chatRoom = Connection.objects.get(request=requestInstance).chatRoom
    if request.user not in [chatRoom.mentor, chatRoom.student]:
        return JsonResponse({"error": "Authorization error"}, status=403)
    messages = chatRoom.messages.all()
    return JsonResponse({"messages": messages}, status=200)

def send_message(request, id):
    response = checkRequest(request)
    if response is not None:
        return response
    if Request.objects.filter(id=id) is None:
        return JsonResponse({"error": "Request doesn't exist"}, status=400) 
    requestInstance = Request.objects.get(id=id)
    if Connection.objects.filter(request=requestInstance) is None:
        return JsonResponse({"error": "Authorization error"}, status=403) 
    chatRoom = Connection.objects.get(request=requestInstance).chatRoom
    if request.user not in [chatRoom.mentor, chatRoom.student]:
        return JsonResponse({"error": "Authorization error"}, status=403)
    
    data = json.loads(request.body)
    if not data.get("content"):
        return JsonResponse({"error": "Message can't be empty."})
    Message.objects.create(chatRoom, request.user, data["content"])
    return JsonResponse({"success": "Message sent successfully."}, status=200)

def profile(request, username):
    if User.objects.filter(username=username) is None:
        return JsonResponse({"error": "Profile doesn't exist."}, status=400) 
    user = User.objects.get(username=username)
    profile = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "about": user.about,
        "skills": [],
        "pictureURL": user.picture.url()
    }
    for skill in user.skills:
        profile["skills"].append(skill.skill)
    return JsonResponse({"profile": profile}, status=200)

def personal_profile(request):
    response = checkRequest(request, post=False)
    if response is not None:
        return response
    user = request.user
    profile = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "about": user.about,
        "skills": [],
        "availableBalance": user.availableBalance(),
        "onHoldBalance": user.onHoldBalance(),
        "totalBalance": user.totalBalance(),
        "pictureURL": user.picture.url()
    }
    for skill in user.skills:
        profile["skills"].append(skill.skill)
    return JsonResponse({"profile": profile}, status=200)

def edit_profile(request):
    response = checkRequest(request)
    if response is not None:
        return response
    data = json.loads(request.body)
    if data.get("first_name") is None:
        data["first_name"] = request.user.first_name
    if data.get("last_name") is None:
        data["last_name"] = request.user.last_name
    if data.get("about") is None:
        data["about"] = request.user.about
    if data.get("phone") is None:
        data["phone"] = request.user.phone
    if data.get("email") is None:
        data["email"] = request.user.email

    userForm = EditUserForm(data)
    if not userForm.is_valid():
        return JsonResponse({"error": checkFormErrors(userForm)[0]})
    request.user.first_name = data["first_name"]
    request.user.last_name = data["last_name"]
    request.user.about = data["about"]
    request.user.phone = data["phone"]
    request.user.email = data["email"]
    request.user.save()
    if data.get("skills"):
        skills = request.user.skills
        for skill in skills:
            skill.delete()
        for skillName in data["skills"]:
            skill = Skill(request.user, skillName)
            try:
                skill.save()
            except Exception:
                continue
    if request.FILES.get("picture"):
        try:
            request.user.picture = request.FILES["picture"]
            request.user.save()
        except Exception:
            return JsonResponse({"error": "Picture is invalid"})
        request.user.save()
    return JsonResponse({"success": "Profile edited successfully"}, status=200)

def notifications(request):
    response = checkRequest(request, post=False)
    if response is not None:
        return response
    notifications = request.user.notifications.all()
    # data = json.loads(request.body)
    # size = len(notifications);
    # fromIndex =  data["fromIndex"] if data.get("fromIndex") else 1
    # toIndex = data["toIndex"] if data.get("toIndex") else size
    # fromIndex -= 1
    # toIndex -= 1
    # if not inBounds(fromIndex, 0, size - 1) or not inBounds(toIndex, fromIndex, size - 1):
    #     return JsonResponse({"error": "Invalid range"}, status=400)
    # notifications = notifications[fromIndex: toIndex]
    return JsonResponse({"notifications": notifications}, status=200)

def messages(request):
    response = checkRequest(request, post=False)
    if response is not None:
        return response
    messages = []
    for room in request.user.student_chatrooms + request.user.mentor_chatrooms:
        if room.messages.exclude(sender=request.user).exists():
            message = room.messages.exclude(sender=request.user).order_by("-timestamp")[0]
            message.request_id = message.connections.all()[0].request.id
            messages.append(message)
    # data = json.loads(request.body)
    # size = len(messages);
    # fromIndex =  data["fromIndex"] if data.get("fromIndex") else 1
    # toIndex = data["toIndex"] if data.get("toIndex") else size
    # fromIndex -= 1
    # toIndex -= 1
    # if not inBounds(fromIndex, 0, size - 1) or not inBounds(toIndex, fromIndex, size - 1):
    #     return JsonResponse({"error": "Invalid range"}, status=400)
    # messages = messages[fromIndex: toIndex]
    return JsonResponse({"messages": messages}, status=200)

