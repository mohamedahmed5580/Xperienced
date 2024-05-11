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
    path('profile/<str:username>',views.profile_view, name="profile"),
    path('balance', views.balance_view, name="balance"),

    # API
    path('api/login', views.login),
    path('api/signup', views.signup),
    path('api/verify_email/send', views.send_email_token),
    path('api/verify_email/verfiy', views.verify_email),
    path('api/new_request', views.new_request),
    path('api/requests', views.requests),
    path('api/requests/categories', views.categories),
    path('api/requests/types', views.types),
    path('api/requests/<int:id>', views.request),
    path('api/requests/<int:id>/cancel', views.cancel_request),
    path('api/requests/<int:id>/complete', views.complete_request),
    path('api/requests/<int:id>/offers', views.offers),
    path('api/requests/<int:id>/offers/add', views.add_offer),
    path('api/requests/<int:id>/offers/<int:offer_id>', views.offer),
    # check balance before accepting
    path('api/requests/<int:id>/offers/<int:offer_id>/accept', views.accept_offer),
    path('api/requests/<int:id>/offers/<int:offer_id>/cancel', views.cancel_offer),
    path('api/requests/<int:id>/chat', views.chat_messages),
    path('api/requests/<int:id>/chat/send', views.send_message),
    path('api/profile/<str:username>', views.profile),
    path('api/profile', views.personal_profile),
    path('api/profile/edit', views.edit_profile),
    path("api/notifications", views.notifications),
    path("api/messages", views.messages),
]