from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django import forms
# class User(AbstractUser):
#     id = models.IntegerField(primary_key=True)
#     USERNAME_FIELD = 'username'
#     username = models.CharField(max_length=100, unique=True, default='username')
#     email = models.EmailField(default='example@example.com')
#     password = models.CharField(max_length=50, default='password', null=False)
#     password1 = models.CharField(max_length=50, default='password', null=False)
#     phone = models.CharField(max_length=50, blank=True, null=True)
#     first_name = models.CharField(max_length=50, blank=True, null=True)
#     last_name = models.CharField(max_length=50, blank=True, null=True)
#     description = models.TextField( blank=True ,null=True)
#     groups = models.ManyToManyField(Group,related_name='custom_user_set_user',blank=True,help_text='The groups this user belongs to.',verbose_name='groups',)
#     user_permissions = models.ManyToManyField(Permission,related_name='custom_user_permissions_set_user', blank=True,help_text='Specific permissions for this user.',verbose_name='user permissions',)
#     image=models.ImageField(upload_to='image/', default='image/user.png', blank=True,null=True)
#     def __str__(self):
#         return self.username
class User(AbstractUser):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, default='username')
    email = models.EmailField(default='example@example.com')
    password = models.CharField(max_length=50, default='password', null=False)
    password1 = models.CharField(max_length=50, default='password', null=False)
    phone = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set_user', blank=True, help_text='The groups this user belongs to.', verbose_name='groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set_user', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')
    image = models.ImageField(upload_to='image/', default='image/user.png', blank=True, null=True)
    def __str__(self):
        return self.username
# Create your models here.
class Skill(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    skill = models.CharField(max_length=50)

class Application(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

