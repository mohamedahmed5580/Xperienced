from django import forms
from .models import Offer,Type,Category

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'salary', 'status']


# [('Full Time', 'full time'), ('Part Time', 'part time')]

# from django.db import models
# from account.models import User

# class Type(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="type",null=True,blank=True)
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name

# class Category(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category",null=True,blank=True)
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name

# class Offer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offer",null=True,blank=True)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     salary = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.ForeignKey(Type, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
#     file = models.FileField(upload_to='offers/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

