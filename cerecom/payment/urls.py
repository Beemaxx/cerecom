from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'payment'



urlpatterns = [
    path('', views.Payment_Cart, name = 'home'),
    path('orderplaced/', views.order_placed, name = 'order_placed'),
    path('webhook/', views.stripe_webhook),

]
