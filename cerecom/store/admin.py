from django.contrib import admin
from django.contrib.admin import ModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Product_Category, Product_Inventory, Product, Product_Discount

    
class ProductResource(resources.ModelResource):
    
    class Meta:
        model = Product
        
        
class ModelAdmin(ImportExportModelAdmin):
    list_display = ['name', 'price', 'origin', 'in_stock', 'created_at', 'modified_at', 'discount_id']
    list_filter = ['in_stock']
    list_editable = ['in_stock', 'price', 'discount_id']
    prepopulated_fields = {'slug': ('name',)}
    resource_class = ProductResource

@admin.register(Product_Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Product)
class ProductAdmin(ModelAdmin):
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

    
    """_summary_
    """