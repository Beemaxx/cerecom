from django.contrib import admin

# Register your models here.
from .models import Product_Category, Product_Inventory, Product, Product_Discount

@admin.register(Product_Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'origin', 'in_stock', 'created_at', 'modified_at', 'discount_id']
    list_filter = ['in_stock']
    list_editable = ['in_stock', 'price', 'discount_id']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product_Inventory)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['vendor','quantity']

@admin.register(Product_Discount)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'discount_percent']
    list_filter = ['active', 'discount_percent']
    list_editable = ['active', 'discount_percent']
    prepopulated_fields = {'desc': ('name',)}