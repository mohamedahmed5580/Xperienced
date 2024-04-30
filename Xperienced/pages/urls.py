from . import views
from django.urls import path,include

urlpatterns = [
    path('home',views.index,name="home"),
    path('login',views.login,name="login"),
    path('signup',views.signup,name="signup"),
    path('find',views.find_Assistant,name="find_Assistant"),
    path('offer',views.offer_Help,name="offer_Help"),
    path('profile',views.profile,name="profile"),
    path('addoffer',views.addOffer,name="addoffer"),
    path('balance',views.Account_Balance,name="balance"),
]