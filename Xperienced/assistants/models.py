from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from random import randint
from datetime import datetime
from django.urls import reverse
from account.models import User
OPEN = "Open"
PENDING = "Pending"
PROGRESS = "In progress"
COMPLETED = "Completed"
CANCELLED = "Cancelled"


class Type(models.Model):
    name = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=100)
    requestType = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="categories")

class Request(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="requests")
    requestType = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="requests")
    budget = models.IntegerField()
    cancelled = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def state(self):
        if self.cancelled:
            return "Cancelled"
        for offer in self.offers.all():
            if offer.state in [PROGRESS, COMPLETED]:
                return offer.state
        return OPEN

    def acceptOffer(self, offer):
        if offer.request != self or self.state() != OPEN:
            return False
        offer.state = PROGRESS
        offer.save()
        chatRoom = ChatRoom(self.owner, offer.bidder)
        chatRoom.save()
        connection = Connection(self, offer, chatRoom)
        connection.save();
        return True

    def cancelOffer(self, offer):
        if offer.request != self or offer.state != PENDING:
            return False
        offer.state = CANCELLED
        offer.save()
        return True

    def completeRequest(self):
        if self.state() != PENDING:
            return False
        offer = self.offers.get(state=PENDING)
        offer.state = COMPLETED
        offer.save()
        return True
    
    def cancelRequest(self):
        if self.state() != OPEN:
            return False
        self.cancelled = True
        self.save()
        return True   

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
    datetime = models.DateTimeField(auto_now_add=True)

class ChatRoom(models.Model):
    student = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="student_chatrooms")
    mentor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="mentor_chatrooms")
    datetime = models.DateTimeField(auto_now_add=True)

    def clean(self, *args, **kwargs):
        if self.student == self.mentor:
            raise ValidationError
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def sendMessage(self, sender, content):
        if sender not in [self.firstUser, self.secondUser]:
            return False
        message = Message(self, sender, content)
        message.save()
        return True

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="sent_messages")
    content = models.TextField(max_length=1000)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Connection(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="connections")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="connections")
    chatRoom = models.ForeignKey(ChatRoom, on_delete=models.RESTRICT, related_name="connections")
    datetime = models.DateTimeField(auto_now_add=True)

    def mentor(self):
        return self.offer.bidder
    def student(self):
        return self.offer.request.owner
    def isActive(self):
        return self.offer.state == PROGRESS

class Token(models.Model):
    TOKEN_VALIDITY_LIMIT = 5
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    key = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def generateTokenKey(self):
        self.key = 0
        for i in range(6):
            self.key += 10**i * randint(0, 9)

    def isExpired(self):
        minitesDiff = (datetime.now() - self.timestamp).total_seconds() / 60.0
        return minitesDiff > self.TOKEN_VALIDITY_LIMIT

def URLValidator(url):
    try:
        reverse(url)
    except Exception:
        raise ValidationError
        
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    content = models.TextField(max_length=250)
    url = models.CharField(max_length=50, validators=[URLValidator])
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="from_transations")
    to_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="to_transations")
    amount = models.IntegerField()
    onHold = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def finalizeTransaction(self):
        if not self.onHold:
            return False
        self.to_user.balance += self.amount
        self.onHold = False
        self.save()