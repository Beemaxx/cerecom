from unicodedata import category
from django.shortcuts import render, get_object_or_404
from requests import get
from .models import Product_Category, Product
from django.views.generic import ListView, DetailView
# Create your views here.




def all_products(request):
    
    products = Product.products.all() #changes to query only product which is active. 
    
    return render(request, 'store/home.html', { 'products': products })


def product_detail(request, slug):
    
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    
    return render(request, 'store/products/detail.html', { 'product': product })


def category_list(request, category_slug):
    
    qr_category = get_object_or_404(Product_Category, slug = category_slug)
    qr_product = Product.objects.filter(category_id = qr_category)
    
    context = { 'category': qr_category,
                'product': qr_product, 
               }
    
    return render(request, 'store/categories/category_list.html', context )


# class CategoryDetailView(DetailView):
    
#     model = Product_Category
#     template_name = 'store/categories/category_detail.html'
    
    
# class CategoryListView(ListView):
    
#     model = Product_Category
#     template_name = 'store/categories/category_list.html'
#     context_object_name = 'category_list'
