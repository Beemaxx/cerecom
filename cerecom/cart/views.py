from cgitb import reset
from math import prod
from urllib import response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
# Create your views here.


  
def cart_summary(request):
    
    template_name = "store/cart/summary.html"
    
    cart = Cart(request)
    context = { "cart_items" : cart }
    
    return render(request,template_name, context )

def cart_add(request):
    
    cart = Cart(request)
    
    if request.POST.get('action') == 'add':
        product_id = int(request.POST.get('productid'))
        product_quantity = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id = product_id)
        cart.add(product = product, qty = product_quantity )
        
    
        cartqty = cart.__len__()
        print(cartqty)    
        response = JsonResponse({'qty': cartqty})
        
        return response
    
def cart_delete(request):
    
    cart = Cart(request)
    
    if request.POST.get('action') == 'delete':

        product_id = int(request.POST.get('productid'))
        cart.delete(product = product_id)
         
        cartqty = cart.__len__()
        print(cartqty)    
        response = JsonResponse({'qty': cartqty})        
        return response
        
        
def cart_item_increase(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'item_increase':
        
            product_id = int(request.POST.get('productid'))
            product_quantity = int(request.POST.get('productqty'))

            cart.item_increase(product = product_id, qty=product_quantity)
            cartqty = cart.__len__()

         
            cartqty = cart.__len__()
            print(cartqty)    
            response = JsonResponse({'qty': cartqty})    
            
    return response


        
def cart_item_decrease(request):

    cart = Cart(request)
    if request.POST.get('action') == 'item_decrease':
    
        product_id = int(request.POST.get('productid'))
        product_quantity = int(request.POST.get('productqty'))

        cart.item_decrease(product = product_id, qty=product_quantity)
         
        cartqty = cart.__len__()
        print(cartqty)    
        response = JsonResponse({'qty': cartqty})
    return response

def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'update_cart':
        
        product_id = int(request.POST.get('productid'))
        product_quantity = int(request.POST.get('productqty'))

        cart.update(product = product_id, qty=product_quantity)
         
        cartqty = cart.__len__()
        print(cartqty)    
        response = JsonResponse({'qty': cartqty})
        
    return response