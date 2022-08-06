
from urllib import response
import json
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
import stripe
from order.views import payment_confirmation
stripe.api_key = 'sk_test_51JPovwI5VK2lgzs7EKjqxgX8HOXez7WuVyHtNJln6JOEjw2osd7IwyZ2XJSia2Kv1fdXWZ6gYObL9MNfJ8Mi3u7H00uPCcSyPR'
endpoint_secret = 'whsec_63ce653a79e541729a93ee764155dca0dc98b214446756f291b43c0b4fd37909'
@login_required
def Payment_Cart(request):
    
    template_name = 'store/payment/home.html'
    x = request.session['shipping_cost']
    cart = Cart(request) #get data from session
    cart_total = cart.get_total_price()
     
    cost_include_shipping = int(cart_total) + int(x)
    cost_include_shipping = str(cost_include_shipping)
    cost_include_shipping = cost_include_shipping.replace('.', '')
    cost_include_shipping = int(cost_include_shipping)
    
    stripe.api_key 
    intent = stripe.PaymentIntent.create(
        amount = cost_include_shipping,
        currency = 'vnd',
        metadata = {'userid': request.user.id }
    )
    
    return render(request, template_name, {'client_secret': intent.client_secret})


@login_required
def order_placed(request):
    
    cart = Cart(request)
    cart.clear()
    template_name = 'store/payment/orderplaced.html'
    
    return render(request, template_name)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    
    if event.type == 'payment_intent.created':
        print('Payment intend was created')
        
    if event.type == 'payment_intent.succeeded':
            payment_confirmation(event.data.object.client_secret)
    
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)