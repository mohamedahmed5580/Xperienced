from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('signup', views.signup_view, name="signup"),
    path('logout', views.logout_view, name="logout"),

    path('new_request', views.new_request_view, name="new_request"),
    path('request/<int:id>', views.request_view, name="request"),
    path('requests', views.requests_view, name="requests"),

    # under development
    path('massage',views.massages,name="massage"),
    path('balance', views.account_balance, name="balance"),

    #API
    path('api/login', views.login),
    path('api/signup', views.signup),
    path('api/verify_email/send', views.send_email_token),
    path('api/verify_email/verfiy', views.verify_email),
    path('api/notifications',views.notifications),
    path('api/new_request', views.find_assistant),
    path('api/requests', views.requests),
]