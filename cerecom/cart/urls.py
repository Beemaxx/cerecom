from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'cart'



urlpatterns = [
    path('', views.cart_summary, name = 'cart_summary'),
    path('add/', views.cart_add, name = 'cart_add'),
]
