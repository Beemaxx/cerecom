from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'store'



urlpatterns = [
    path('', views.all_products, name = 'all_products'),

    path('product/<slug:slug>/', views.product_detail, name = 'product_detail'),
    
    path('category/<slug:category_slug>/', views.category_list, name = 'category_list'),
    
    # path('search/', views.SearchResultView.as_view() , name='search_result'),
    path('search/', views.search_result , name='search_result'),

    # path('category/', views.CategoryListView.as_view() , name = 'category_list'),
    # path('category/<slug:category_slug>/', views.CategoryDetailView.as_view() , name = 'category_detail'),

]
