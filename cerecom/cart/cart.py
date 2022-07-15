from decimal import Decimal
from store.models import Product


class Cart():
    
    def __init__(self, request):
        
        self. session = request.session 
        cart = self.session.get('skey')
        
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
            
        self.cart = cart
        
        
        
    def add(self, product, qty):
        
        product_id = str(product.id)
        print(product_id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] += qty

        else:
            self.cart[product_id] = {'price': product.price, 'qty': qty }
            
        self.save()
        
    def item_increase(self, product, qty):
            
        product_id = str(product)
        print(product_id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] += 1

        else:
            self.cart[product_id] = {'price': product.price, 'qty': qty }
            
        self.save()
        
    def item_decrease(self, product, qty):
            
        product_id = str(product)
        print(product_id)
        if product_id in self.cart:
                self.cart[product_id]['qty'] -= 1
                
                if self.cart[product_id]['qty'] == 0:
                    
                    del self.cart[product_id]    
        else:
            self.cart[product_id] = {'price': product.price, 'qty': qty }
            
        self.save()
    
    def delete(self, product):
        
        """
        Dekete Item from session data
        """
        
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]          
            self.save()
        
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product']= product
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
             
            
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
    
    def save(self):
        self.session.modified = True