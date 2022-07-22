from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .forms import UserLoginForm
from . import views

app_name = 'account'



urlpatterns = [
    path('register/', views.account_registration, name = 'register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
   
    #User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    #User login view
    path('login/', auth_views.LoginView.as_view(
        template_name='store/account/registration/login.html',
        form_class = UserLoginForm,
        ), name='login'),  
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
