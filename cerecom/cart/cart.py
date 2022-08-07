from decimal import Decimal

from django.conf import settings
from store.models import Product
from django.conf import settings

class Cart():
    
    def __init__(self, request):
        
        self.session = request.session 
        cart = self.session.get(settings.CART_SESSION_ID)
        shipping_cost = self.session.get('shipping_cost')
        print(shipping_cost)
        
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
            
        self.cart = cart
        
        
        
    def add(self, product, qty):
        
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] += qty

        else:
            
            #generate item into cart session

            self.cart[product_id] = {'price': product.price, 'qty': qty , 'promotion_price': product.get_product_promotion_price}

            
        self.save()
        
    def add_shipping_cost(self, shipping_cost):
        
        self.cart['shipping_cost'] = shipping_cost


        self.save()
        
    def item_increase(self, product, qty):
            
        product_id = str(product)
        print(product_id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] += 1

        else:
            self.cart[product_id] = {'price': product.price, 'qty': qty, 'promotion_price': product.get_product_promotion_price}
            
        self.save()
        
    def item_decrease(self, product, qty):
            
        product_id = str(product)
        print(product_id)
        if product_id in self.cart:
                self.cart[product_id]['qty'] -= 1
                
                if self.cart[product_id]['qty'] == 0:
                    
                    del self.cart[product_id]    
        else:
            #generate item into cart session
            self.cart[product_id] = {'price': product.price, 'qty': qty, 'promotion_price': product.get_product_promotion_price }
            
        self.save()
    
    def delete(self, product):
        
        """
        Dekete Item from session data
        """
        
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]          
            self.save()
            
    def update(self, product, qty):
        
        product_id = str(product)
        
        if product_id in self.cart:
            
            self.cart[product_id]['qty'] = qty
            
        self.save()
        
    def clear(self): 
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()
        print(self.cart.values())
        print(self.cart.keys())

        
        for product in products:
            cart[str(product.id)]['product']= product
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['promotion_price'] = Decimal(item['promotion_price'])
            item['total_price'] = item['promotion_price'] * item['qty']
            yield item
             
            
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.cart.values())
    
    
    def get_total_order(self):
        
        order_total = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

        return order_total
    
    def get_total_price(self):
        
        subtotal = sum(Decimal(item['promotion_price']) * item['qty'] for item in self.cart.values())
        
        return str(subtotal)
    

    
    def discount_amount(self):
        order_total = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
        subtotal = sum(Decimal(item['promotion_price']) * item['qty'] for item in self.cart.values())

        amount = order_total - subtotal
        return amount    
    
    def save(self):
        self.session.modified = True
        
    def get_price_with_shipping(self):
        
        shipping_cost = self.session['shipping_cost']
        
        subtotal = sum(Decimal(item['promotion_price']) * item['qty'] for item in self.cart.values())
        
        final = int(shipping_cost) + int(subtotal)
        
        return final