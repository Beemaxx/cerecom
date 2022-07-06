from unicodedata import category
from django.shortcuts import render, get_object_or_404
from .models import Product_Category, Product
# Create your views here.


def all_categories(request):
    
    return {
         'product_categories' : Product_Category.objects.all() 
    }



def all_products(request):
    
    products = Product.objects.all() 
    
    return render(request, 'store/home.html', { 'products': products })


def product_detail(request, slug):
    
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    
    return render(request, 'store/products/detail.html', { 'product': product })