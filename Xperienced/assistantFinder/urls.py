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
    path('balance', views.balance_view, name="balance"),
    # path('profile/<str:username>',views.profile, name="profile"),
    path('profile/<str:username>',views.profile, name="profile"),

    # under development
    path('profile',views.temp_profile, name="profile"),
    

    path('request', views.request_view, name="request"),
    # path('find', views.find_assistant, name="find_assistant"),
    # path('offer', views.offer_help, name="offer_help"),

    path('balance', views.balance_view, name="balance"),
    #API
    path('api/login', views.login),
    path('api/signup', views.signup),
    path('api/verify_email/send', views.send_email_token),
    path('api/verify_email/verfiy', views.verify_email),
    path('api/new_request', views.new_request),
    path('api/requests', views.requests),
    path('api/request/<int:id>/offer', views.add_offer),
    # path('api/request/<int:id>/accept_offer', views.accept),
    path('api/request/<int:id>/chat/send', views.send_message),
]