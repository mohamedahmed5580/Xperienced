from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from phonenumber_field import PhoneNumberField

class User(AbstractUser):
    phoneNumber = PhoneNumberField()

class RequestType(models.Model):
    name = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=100)
    requestType = models.ForeignKey(RequestType, on_delete=models.CASCADE, related_name="categories")

class Request(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="requests")
    budget = models.IntegerField()
    state = models.CharField(max_length=100, choices=[
        ("Open", "Open"), 
        ("In progress", "In progress"), 
        ("Cancelled", "Cancelled"), 
        ("Completed", "Completed")
        ])

class Offer(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="offers")
    bid = models.IntegerField()
    notes = models.TextField(max_length=200)

class Connection(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="connections")
    date = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="messages")
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, related_name="messages")
    