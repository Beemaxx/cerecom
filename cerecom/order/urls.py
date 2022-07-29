from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'order'



urlpatterns = [
    path('add/', views.add, name = 'add'),
    path('payment_confirmation/', views.payment_confirmation, name = 'payment_confirmation'),
    path('<str:order_key>/', views.order_detail, name = 'order_detail'),

]
