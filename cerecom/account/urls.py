from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'account'



urlpatterns = [
    path('register/', views.account_registration, name = 'register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
   
    #User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

]
