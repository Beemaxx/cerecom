from tempfile import tempdir
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm
from . import views
from django.views.generic import TemplateView

app_name = 'account'



urlpatterns = [
    path('register/', views.account_registration, name = 'register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
   
    #User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete/', views.delete_users, name='delete_users'),
    
    
    #Password Reset Complete
    #Page to input password reset email
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='store/account/user/password_reset_email_input.html',
        success_url='password_reset_email_confirm',
        email_template_name='store/account/user/password_reset_email.html',
        form_class=PwdResetForm,
        ), name='password_reset'),
    
    #Page to input new password
    path('password_reset/<slug:uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'store/account/user/password_reset_new_pwd_input.html',
        success_url='/account/password_reset/password_reset_complete/',
        form_class=PwdResetConfirmForm,
        ), name='password_reset_confirm'),
    
    #Page to send status that the password instruction was sent via email.
    path('password_reset/password_reset_email_confirm/', TemplateView.as_view(
        template_name='store/account/user/status_confirmation.html',
    ), name = 'password_reset_email_confirm'),
    
    #Page to indicate the password reset was successful.
    path('password_reset/password_reset_complete/', TemplateView.as_view(
        template_name='store/account/user/status_confirmation.html',
        ), name = 'password_reset_complete'),
    

    #User login view
    path('login/', auth_views.LoginView.as_view(
        template_name='store/account/registration/login.html',
        form_class = UserLoginForm,
        ), name='login'),  
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/delete/confirm/', TemplateView.as_view(
        template_name = 'store/account/user/delete_confirm.html'), name='delete_confirm'),
]
