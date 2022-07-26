from ast import Or
import re
from urllib import response
from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http.response import JsonResponse
from cart.cart import Cart
from .models import Order, OrderItems

def add(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        
        user_id = request.user.id
        order_key = request.POST.get('order_key')
        cart_total = cart.get_total_price()
        
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else: 
            order = Order.objects.create(
                user_id = user_id,
                full_name='name',
                shipping_address1 = 'add1',
                shipping_address2 = 'add2',
                total_paid = cart_total,
                order_key = order_key,
            )
            
            order_id = order.pk
            
            for item in cart:
                OrderItems.objects.create(
                    order_id=order_id, 
                    product=item['product'], 
                    price=item['price'],
                    quantity=item['qty'])
                
        response = JsonResponse({'success': 'Order was created'})
            
        return response
            



def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
    
    
def user_orders(request):
    
    user_id = request.user.id
    completed_orders = Order.objects.filter(user_id=user_id)
    
    return completed_orders