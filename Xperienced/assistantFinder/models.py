from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from random import randint
from datetime import datetime
from django.urls import reverse

OPEN = "Open"
PENDING = "Pending"
PROGRESS = "In progress"
COMPLETED = "Completed"
CANCELLED = "Cancelled"

class User(AbstractUser):
    phone = PhoneNumberField()
    verifiedEmail = models.BooleanField(default=False)

    def createToken(self):
        if Token.objects.filter(user=self).exists():
            Token.objects.get(user=self).delete()
        token = Token(self)
        token.generateTokenKey()
        token.save()
        return token.key
    
    def getToken(self):
        return Token.objects.filter(user=self)

    def verifyEmail(self):
        Token.objects.get(user=self).delete()
        verifiedEmail = True

class Category(models.Model):
    name = models.CharField(max_length=100)
    requestType = models.CharField(max_length=25, choices=[
        ("Academic Support", "Academic Support"), 
        ("Mentorship", "Mentorship")
        ])

class Request(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="requests")
    budget = models.IntegerField()
    cancelled = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def state(self):
        if self.cancelled:
            return "Cancelled"
        for offer in self.offers:
            if offer.state in [PROGRESS, COMPLETED]:
                return offer.state
        return OPEN

    def acceptOffer(self, offer):
        if offer.request != self or self.state() != OPEN:
            return False
        offer.state = PROGRESS
        return True

    def cancelOffer(self, offer):
        if offer.request != self or offer.state != PENDING:
            return False
        offer.state = CANCELLED
        return True

    def completeRequest(self):
        if self.state() != PENDING:
            return False
        offer = self.offers.get(state=PENDING)
        offer.state = COMPLETED
    
    def cancelRequest(self):
        if self.state() != OPEN:
            return FALSE
        self.cancelled = True
        

class Offer(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="offers")
    bid = models.IntegerField()
    notes = models.TextField(max_length=200)
    state = models.CharField(max_length=100, default=PENDING, choices=[
        (PENDING, PENDING), 
        (PROGRESS, PROGRESS), 
        (CANCELLED, CANCELLED), 
        (COMPLETED, COMPLETED)
        ])
    date = models.DateTimeField(auto_now_add=True)

class Connection(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="connections")
    date = models.DateTimeField(auto_now_add=True)

    def instructor(self):
        return self.offer.request.owner
    def student(self):
        return self.offer.bidder
    def isActive(self):
        return self.offer.state == PROGRESS

class Message(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(max_length=1000)
    byInstructor = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def sender(self):
        return self.connection.instructor() if self.byInstructor else self.connection.student()

class Token(models.Model):
    TOKEN_VALIDITY_LIMIT = 5
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    key = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def generateTokenKey(self):
        self.token = 0
        for i in range(6):
            self.token += 10**i * randint(0, 9)

    def isExpired(self):
        minitesDiff = (datetime.now() - self.date).total_seconds() / 60.0
        return minutesDiff > TOKEN_VALIDITY_LIMIT

def URLValidator(url):
    try:
        reverse(url)
    except Exception:
        raise ValidationError
        
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    content = models.TextField(max_length=250)
    url = models.CharField(max_length=50, validators=[URLValidator])