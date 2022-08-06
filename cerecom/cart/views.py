from cgitb import reset
from math import prod
from tkinter.tix import INTEGER
from typing import final
from urllib import response
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from graphene import Decimal
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from requests import request
# Create your views here.


@login_required
def cart_summary(request):
    
    template_name = "store/cart/summary.html"
    
    cart = Cart(request)

    context = { "cart_items" : cart}
    
    return render(request,template_name, context )

@login_required
def cart_add(request):
    
    cart = Cart(request)
    
    print(request.POST.get('product_id'))
          
    if request.POST.get('action') == 'add':
        product_id = int(request.POST.get('productid'))
        product_quantity = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id = product_id)
        cart.add(product = product, qty = product_quantity )
        
    
        cartqty = cart.__len__()
        print(cartqty)    
        response = JsonResponse({'qty': cartqty})
        
        return response

@login_required    
def cart_delete(request):
    
    cart = Cart(request)
    
    if request.POST.get('action') == 'delete':

        product_id = int(request.POST.get('productid'))
        cart.delete(product = product_id)
         
        cartqty = cart.__len__()
        print(cartqty)    
        response = JsonResponse({'qty': cartqty})        
        return response
        
@login_required        
def cart_item_increase(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'item_increase':
        
            product_id = int(request.POST.get('productid'))
            product_quantity = int(request.POST.get('productqty'))

            cart.item_increase(product = product_id, qty=product_quantity)
            cartqty = cart.__len__()
            print(cartqty)    
            response = JsonResponse({'qty': cartqty})    
            
    return response


@login_required        
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

@login_required
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

@login_required
def add_shipping_cost(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'add_shipping_cost':
    
        shipping_cost = request.POST.get('shipping_cost')
        request.session['shipping_cost'] = shipping_cost
        
        x = request.session['shipping_cost']
        print(type(x))
        
        print('shipping cost ' + shipping_cost)
        final_cost = cart.get_total_price()

        print(type(final_cost))

        
        print('final cost ' + final_cost)
        
        cost_include_shipping = int(final_cost) + int(x)
     
        
        response = JsonResponse(
            {'final_cost': cost_include_shipping},
            )

    # cart = Cart(request)
    # print(request.session.keys())
        
    # if request.POST.get('action') == 'add_shipping_cost':
        
    #     shipping_cost = int(request.POST.get('shipping_cost'))
    #     print(shipping_cost)
    #     final_cost = cart.get_total_price(shipping_cost=shipping_cost )
    #     print(final_cost)
    #     response = HttpResponse({'final_cost': final_cost})
    # else: 
    #     response = None
        
    return response 