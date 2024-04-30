from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('login/submit', views.login, name="login_submit"),
    path('signup', views.signup_view, name="signup"),
    path('signup/submit', views.signup, name="signup_submit"),
    path('logout', views.logout_view, name="logout"),

    path('find', views.find_assistant, name="find_assistant"),
    path('offer', views.offer_help, name="offer_help"),
    path('profile', views.profile, name="profile"),
    path('request', views.add_offer, name="add_offer"),
    path('balance', views.account_balance, name="balance"),
]