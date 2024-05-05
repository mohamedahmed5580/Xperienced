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
    path('notifications',views.notifications_view, name="notifications"),
    path('messages',views.messages_view, name="messages"),
    # path('profile/<str:username>',views.profile, name="profile"),

    path('request', views.request_view, name="request"),
    path('massage',views.massages,name="massage"),
    path('find', views.find_assistant, name="find_assistant"),
    path('offer', views.offer_help, name="offer_help"),
    
    path('profile', views.profile, name="profile"),
    # path('notification',views.notification,name="notification"),
    path('massage',views.massages,name="massage"),

    path('balance', views.account_balance, name="balance"),

    #API
    path('api/login', views.login),
    path('api/signup', views.signup),
    path('api/verify_email/send', views.send_email_token),
    path('api/verify_email/verfiy', views.verify_email),
    path('api/notifications',views.notifications),
    path('api/messages',views.messages),
    path('api/new_request', views.new_request),
    path('api/requests', views.requests),
]