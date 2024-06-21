from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('request/<int:id>', views.request_view, name="request"),
    path('offers', views.offer_view, name="offers"),
    path('myoffer/<int:id>/', views.myoffer_view, name="myoffer"),
    path('myoffer/delete_offer/<int:id>', views.delete_offer, name="delete_offer"),
    path('sendoffers', views.offers, name="sendoffers"),
    path('notifications',views.notifications_view, name="notifications"),
    path('messages',views.messages_view, name="messages"),
    path('balance', views.balance_view, name="balance"),
    path('new_request', views.add_offer, name="new_offer"),
   
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)\

