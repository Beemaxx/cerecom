from ast import Or
from tabnanny import verbose
from django.db import models
from django.urls import reverse
from store.models import Product_Discount


# Create your models here.

from decimal import Decimal
from django.conf import settings
from store.models import Product
from account.models import UserBase

class Order(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=50)
    default_address = UserBase.address_line_1
    shipping_address1 = models.CharField(max_length=250)
    shipping_address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    post_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=12, decimal_places=0)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created_at', )
        verbose_name = "Order"
        verbose_name_plural = "Order"
        
    def __str__(self):
        return str(self.created_at)
    
    def get_absolute_url(self):
        return reverse('order:order_detail', args=[self.order_key])
    
    @property
    def get_order_cost(self):
        order_cost = Decimal(self.total_paid - 30000)
        return order_cost
    
    
    
class OrderItems(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items",)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_subtotal(self):
        item_subtotal = Decimal(self.quantity * self.price)
        return item_subtotal
    
    class Meta:
        verbose_name = "Order Items"
        verbose_name_plural = "Order Items"
        

class OrderShipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_shipping", default=None)
    shipping_company = models.CharField(max_length=200, default=None)
    shipping_status = models.BooleanField(default=False)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=30000)

    def __str__(self):
        return str(self.order)
    
    class Meta:
        verbose_name = "Order Shipping"
        verbose_name_plural = "Order Shipping"
