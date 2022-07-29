from email import message
from re import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from requests import get
from .models import Product_Category, Product
from django.views.generic import ListView, DetailView
from django.http import response
# Create your views here.




def all_products(request):
    
    products = Product.products.all() #changes to query only product which is active. 
    paginator = Paginator(products, 12)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/home.html', { 'page_obj': page_obj})


def product_detail(request, slug):
    
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    
    return render(request, 'store/products/detail_2.html', { 'product': product })


def category_list(request, category_slug):
    
    qr_category = get_object_or_404(Product_Category, slug = category_slug)
    qr_product = Product.objects.filter(category_id = qr_category)  
    
    paginator = Paginator(qr_product, 12)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/categories/category_list.html', { 'page_obj': page_obj} )


def search_result(request):

    query = request.GET.get("q")
    template_name = 'store/products/search_result.html'

    if query:
        object_list = Product.objects.filter(Q(name__icontains=query)|Q(category_id__name__icontains=query)).order_by('desc')
    else:
        object_list = Product.objects.none()


    paginator = Paginator(object_list, 12)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, template_name, { 'page_obj': page_obj , 'query':query } )


# class SearchResultView(ListView):
    
#     model = Product
#     template_name = 'store/products/search_result.html'
#     paginate_by = 12
#     context_object_name = "object_list"

    
#     def get_queryset(self):

#         query = self.request.GET.get("q")

        
#         if query:
#             object_list = Product.objects.filter(Q(name__icontains=query)|Q(category_id__name__icontains=query)).order_by('desc')
#         else:
#             object_list = self.model.objects.none()
     
        
#         return object_list
    


# class CategoryDetailView(DetailView):
    
#     model = Product_Category
#     template_name = 'store/categories/category_detail.html'
    
    
# class CategoryListView(ListView):
    
#     model = Product_Category
#     template_name = 'store/categories/category_list.html'
#     context_object_name = 'category_list'
