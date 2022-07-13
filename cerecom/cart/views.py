from math import prod
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
# Create your views here.


  
def cart_summary(request):
    
    template_name = "store/cart/summary.html"
        
    return render(request, template_name)

def cart_add(request):
    
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_quantity = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id = product_id)
        cart.add(product = product, qty = product_quantity )
        
    
        cartqty = cart.__len__()
        print(cartqty)    
        response = JsonResponse({'qty': cartqty})
        
        return response

