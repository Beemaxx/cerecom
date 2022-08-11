from django.contrib import admin
from order.models import Order, OrderItems, OrderShipment

# Register your models here.

from django.contrib.admin import AdminSite

class ManagementDashboard(AdminSite):
    site_header = "Management Dashboard"
    site_title = "Management Portal"
    index_title = "Welcome to Management Portal"
    
    
management_dashboard = ManagementDashboard(name="management_dashboard")

class OrderAdmin(admin.ModelAdmin):
    list_display = ["user","total_paid","billing_status"]
    list_filter = ['billing_status']


class ShippingAdmin(admin.ModelAdmin):
    list_display = ["order","shipping_status","shipping_cost"]
    list_filter = ['shipping_status']    


management_dashboard.register(OrderItems)
management_dashboard.register(OrderShipment, ShippingAdmin)
management_dashboard.register(Order , OrderAdmin)