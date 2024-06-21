import json
from django.contrib import auth
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import  logout as auth_logout
from .forms import OfferForm
from .models import Offer,Type, Category
from account.models import User
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

def add_offer(request):
    return render(request, 'pages/find_assistant.html')


def request_view(request, id):
    return render(request, 'pages/add_offer.html')

# def profile_view(request):
#     return render(request, 'pages/profile.html', {
#         "profile": request.user
#     })

def balance_view(request):
    return render(request, 'pages/account_balance.html')

def notifications_view(request):
    return render(request, "pages/Notifications.html")

def offer_view(request):
    details = Offer.objects.all()
    print(details)
    print('All Offer')
    
    return render(request, 'pages/offer_help.html',{'offers': details})

def myoffer_view(request, id):
    user = get_object_or_404(User, id=id)
    offers = Offer.objects.filter(user=user)

    profile = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "password": user.password,
        "description": user.description,
        "image": user.image,
    }
    return render(request, 'pages/My_offer_help.html', {'offers': offers, 'profile': profile})



@login_required
@transaction.atomic
def offers(request):
    print("in offer")
    if request.method == 'POST':
        print(request.POST)
        try:
            # Get or create Type instance
            type_instance, created = Type.objects.get_or_create(user=request.user, name=request.POST['type'])
            if created:
                print(f"Created new Type: {type_instance.name}")
            else:
                print(f"Type already exists: {type_instance.name}")

            # Ensure the type_instance is saved
            if not type_instance.pk:
                type_instance.save()

            # Get or create Category instance
            category_instance, created = Category.objects.get_or_create(user=request.user, name=request.POST['category'])
            if created:
                print(f"Created new Category: {category_instance.name}")
            else:
                print(f"Category already exists: {category_instance.name}")

            # Ensure the category_instance is saved
            if not category_instance.pk:
                category_instance.save()

            # Initialize the form with POST data and files
            form = OfferForm(request.POST, request.FILES)
            
            if form.is_valid():
                offer = form.save(commit=False)
                offer.user = request.user
                offer.type = type_instance
                offer.category = category_instance
                offer.save()  # Save the offer again to update the type and category
                print("Offer created successfully.")
                return redirect('myoffer', id=request.user.id)
            else:
                print("Form is not valid.")
                print(form.errors)
                messages.error(request, "There was an error with your form.")
        except Exception as e:
            print(f"Exception occurred: {e}")
            messages.error(request, "An unexpected error occurred.")
    else:
        form = OfferForm()
    
    return render(request, 'pages/offer_help.html', {'form': form})


@login_required
@transaction.atomic
def delete_offer(request, id):
    print('in delete Offer')
    if request.method == 'POST':
        try:
            offer = Offer.objects.get(id=id, user=request.user)  # Ensure the offer belongs to the user

            types = Type.objects.filter(offer=offer)
            categories = Category.objects.filter(offer=offer)

            types.delete()
            categories.delete()
            offer.delete()

            messages.success(request, "Offer and related objects successfully deleted.")
        except Offer.DoesNotExist:
            messages.error(request, "Offer not found.")
        return redirect('myoffer', id=request.user.id)
    return redirect('myoffer', id=request.user.id)


def messages_view(request):
    return render(request, "pages/Messages.html")

