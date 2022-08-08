from django.contrib import admin
from order.models import Order, OrderItems, OrderShipment

# Register your models here.

from django.contrib.admin import AdminSite

class ManagementDashboard(AdminSite):
    site_header = "Management Dashboard"
    site_title = "Management Portal"
    index_title = "Welcome to Management Portal"
    
    
management_dashboard = ManagementDashboard(name="management_dashboard")

management_dashboard.register(OrderItems)
management_dashboard.register(OrderShipment)
management_dashboard.register(Order)