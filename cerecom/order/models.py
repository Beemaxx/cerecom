from ast import Or
from tabnanny import verbose
from django.db import models

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
    
class OrderItems(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items",)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = "Order Items"
        verbose_name_plural = "Order Items"