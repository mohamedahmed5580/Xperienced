from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('login/submit', views.login),
    path('signup', views.signup_view, name="signup"),
    path('signup/submit', views.signup),
    path('logout', views.logout_view, name="logout"),

    path('verify_email/send', views.send_email_token),
    path('verify_email/verfiy', views.verify_email),

    path('find', views.find_assistant_view, name="find_assistant"),
    path('offer', views.requests_view, name="requests"),
    path('request', views.request_view, name="request"),
    path('profile', views.profile, name="profile"),
    path('notification',views.notification,name="notification"),
    path('massage',views.massages,name="massage"),

    path('balance', views.account_balance, name="balance"),
]