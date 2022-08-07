from ast import Or
import re
from urllib import response
from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http.response import JsonResponse
from cart.cart import Cart
from .models import Order, OrderItems, OrderShipment

def add(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        
        user_id = request.user.id
        order_key = request.POST.get('order_key')
        shipping_cost = request.session['shipping_cost']
        cart_total = cart.get_price_with_shipping()
        no_discount_cost = cart.get_total_order()


        
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
                cost_without_promotion = no_discount_cost,
                
            )
            
            order_id = order.pk
            shipping = OrderShipment.objects.create(
                order_id = order_id,
                shipping_company = "sample company 1",
                shipping_cost = shipping_cost,
            )
            
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


def order_detail(request, order_key):
    
    order_no = Order.objects.filter( order_key = order_key)
    
    print(order_no.values_list())
    
    return render(request, 'store/cart/order_detail.html', {'order_no' : order_no })