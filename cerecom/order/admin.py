from django.contrib import admin

# Register your models here.
from .models import Order, OrderItems, OrderShipment

admin.site.register(Order)
admin.site.register(OrderItems)

@admin.register(OrderShipment)
class  UserBaseAdmin(admin.ModelAdmin):
    list_display = ['order', 'shipping_status']
    list_filter = ['shipping_status']
    list_editable = ['shipping_status']