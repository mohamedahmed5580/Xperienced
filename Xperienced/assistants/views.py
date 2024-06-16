from django.shortcuts import render

# Create your views here.
import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from . import models
from django.core.paginator import Paginator
from django.contrib.auth import  logout as auth_logout
from django.contrib.auth import authenticate, login
from account.models import User

from .models import Request, Offer, User, Category, Type
from .forms import RequestForm, OfferForm  # Assuming you have forms for these models

# from .models import Skill
# Create your views here.

def new_request_view(request):
    return render(request, 'pages/find_assistant.html')
def index(request):
    return render(request, 'pages/index.html')
def register(request):
    return render(request,'pages\signup.html')

def login_view(request):
    return render(request, 'pages/login.html')

def signup_view(request):
    return render(request, 'pages/signup.html')

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))

def new_request_view(request):
    return render(request, 'pages/find_assistant.html')

def requests_view(request):
    return render(request, 'pages/offer_help.html')


def request_view(request, id):
    return render(request, 'pages/add_offer.html')

def profile_view(request):
    return render(request, 'pages/profile.html', {
        "profile": request.user
    })

def balance_view(request):
    return render(request, 'pages/account_balance.html')
    
def notifications_view(request):
    return render(request, "pages/Notifications.html")

# def skills(request):
#     if request.method == 'POST':
#         skill_name = request.POST.get('skill-input')
#         user_id = request.user.id

#         if skill_name and user_id:
#             user = User.objects.get(id=user_id)
#             skill = Skill(user=user, skill=skill_name)
#             skill.save()
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def messages_view(request):
    return render(request, "pages/Messages.html")

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.owner = request.user
            new_request.save()
            return redirect('request_detail', request_id=new_request.id)
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form})

@login_required
def request_detail(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    return render(request, 'request_detail.html', {'request': req})

@login_required
def make_offer(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            new_offer = form.save(commit=False)
            new_offer.bidder = request.user
            new_offer.request = req
            new_offer.save()
            return redirect('request_detail', request_id=request_id)
    else:
        form = OfferForm()
    return render(request, 'make_offer.html', {'form': form, 'request': req})

@login_required
def accept_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    if offer.request.owner == request.user and offer.request.state() == 'Open':
        offer.request.acceptOffer(offer)
        return redirect('request_detail', request_id=offer.request.id)
    return JsonResponse({'status': 'error', 'message': 'Cannot accept offer'}, status=400)

@login_required
def cancel_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    if offer.bidder == request.user and offer.state == 'Pending':
        offer.request.cancelOffer(offer)
        return redirect('request_detail', request_id=offer.request.id)
    return JsonResponse({'status': 'error', 'message': 'Cannot cancel offer'}, status=400)

@login_required
def complete_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if req.owner == request.user and req.state() == 'Pending':
        req.completeRequest()
        return redirect('request_detail', request_id=request_id)
    return JsonResponse({'status': 'error', 'message': 'Cannot complete request'}, status=400)

@login_required
def cancel_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if req.owner == request.user and req.state() == 'Open':
        req.cancelRequest()
        return redirect('request_detail', request_id=request_id)
    return JsonResponse({'status': 'error', 'message': 'Cannot cancel request'}, status=400)
@login_required
def make_offer(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            new_offer = form.save(commit=False)
            new_offer.bidder = request.user
            new_offer.request = req
            new_offer.save()
            return JsonResponse({'status': 'success', 'message': 'Offer submitted successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
    else:
        form = OfferForm()
    return render(request, 'make_offer.html', {'form': form, 'request': req})