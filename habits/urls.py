
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('evaluate/', views.initial_evaluation, name='initial_evaluation'),
    path('profile/', views.profile_view, name='profile'),
    path('history/', views.history_view, name='history'),
]