from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    # path('signin/', views.login_views, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register/signup/', views.signup_view, name='signup'),
    path('adminpage/', views.admin, name='adminpage'),
    path('userpage/', views.user, name='userpage'),
    path('profile/skills', views.skills, name="skills"), 
    # path('profile/',views.profile_view, name="profile"),
    # path('jobs/', views.jobs, name='jobs'), 
    # path('applyForm/<int:job_id>/', views.applyForm, name='applyForm'), 
    # path('appliedJobs/', views.applied_jobs, name="appliedjobs"),
    # path('listjobs/', views.list_jobs, name="listjobs"),
    # path('search', views.search, name="search"),
    # path('profileu', views.proileu, name="profileu"),
    # path('some-url/', views.some_view_function, name='some-view'),
    # path('profile/', views.profile, name='profile'),  
    # path('user_page/',views.user_page,name='user_page'), 
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)