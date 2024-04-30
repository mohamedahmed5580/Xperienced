from django.contrib import admin
from .models import User, Category, Request, Offer, Notification, Token, Message, Connection

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Request)
admin.site.register(Offer)
admin.site.register(Notification)
admin.site.register(Token)
admin.site.register(Message)
admin.site.register(Connection)