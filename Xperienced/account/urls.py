from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name= 'index'),
    path('loginto/', views.login_views, name='login'),
    path('login/', views.login_view, name='login_view'), 
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register/login_view', views.login_view, name='login_view'),
    path('register/signup', views.signup, name='signup'),
    path('profile/',views.profile, name="profile"),
    path('profile/<int:id>',views.profile_view, name="profile"),
    path('profile/',views.profile_view, name="profile"),
    path('profile/skills', views.skills, name="skills"), 
    path('profile/edit', views.edit_profile, name="edit"), 
    path('profile/editabout', views.edit_about, name="editabout"), 
    path('profile/editimage', views.edit_image_profile, name="editimage"), 
    path('profile/skills/delete/<int:skill_id>', views.delete_skill, name='delete_skill'),
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

