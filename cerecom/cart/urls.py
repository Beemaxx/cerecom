from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'cart'



urlpatterns = [
    path('', views.cart_summary, name = 'cart_summary'),
    path('add/', views.cart_add, name = 'cart_add'),
    path('delete/', views.cart_delete, name = 'cart_delete'),
    path('item_increase/', views.cart_item_increase, name = 'item_increase'),
    path('item_decrease/', views.cart_item_decrease, name = 'item_decrease'),

]
