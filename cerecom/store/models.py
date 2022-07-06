from sqlite3 import Timestamp
from tabnanny import verbose
from unicodedata import decimal
from django.db import models
from django.forms import BooleanField
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    

class Product_Inventory(TimeStampedModel):
    vendor = models.CharField(max_length=255, default="")
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name_plural = 'inventory'
        
    def __str__(self):
        return self.vendor 
    
class Product_Discount(TimeStampedModel):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    discount_percent = models.FloatField(default=0)
    active = models.BooleanField(default=False)
        
    class Meta:
        verbose_name_plural = 'discounts'
        
    def __str__(self):
        return self.name
        
class Product_Category(TimeStampedModel):
    
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique = True)
    desc = models.TextField(blank=True)
  
    
    class Meta:
        # verbose_name = 'categories'
        verbose_name_plural = 'categories'
        
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
    
    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    category_id = models.ForeignKey(Product_Category, related_name='product_category', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='product_creator', on_delete=models.CASCADE)
    inventory_id = models.ForeignKey(Product_Inventory, related_name='product_inventory', on_delete=models.CASCADE)
    discount_id = models.ForeignKey(Product_Discount, related_name='product_discount', on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique = True)
    desc = models.TextField(blank=True)
    SKU = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    origin = models.CharField(max_length=255, default='Japan')
    image = models.ImageField(upload_to='images/')
    in_stock = models.BooleanField(default=True)
    
    class Meta: 
        verbose_name_plural = 'Products'
        ordering = ('-created_at', )
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        kwargs = {
            'slug' : self.slug,
        }
        return reverse( 'store:product_detail', kwargs = kwargs)
    