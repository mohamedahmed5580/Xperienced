from django.contrib import admin
from .models import Category, Offer, Type
# from .models import Skill
# # Register your models here.
# admin.site.register(Skill)
admin.site.register(Category)
admin.site.register(Offer)
admin.site.register(Type)