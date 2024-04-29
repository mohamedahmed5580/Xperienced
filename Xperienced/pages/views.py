from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(requst):
    return render(requst,'pages/Indexs.html')

def login(requst):

    return render(requst,'pages/Login.html')

def signup(requst):
    return render(requst,'pages/Signin.html')

def find_Assistant(requst):
    return render(requst,'pages/Find_Assistant.html')

def offer_Help(requst):
    return render(requst,'pages/Offer_Help.html')

def profile(requst):
    return render(requst,'pages/Profile.html')
def addOffer(requst):
    return render(requst,'pages/Add_Offer.html')
def Account_Balance(requst):
    return render(requst,'pages/Account_Balance.html')

def Notification(requst):
    return render(requst,'pages/Notifications.html')