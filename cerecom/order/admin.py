from django.contrib import admin

# Register your models here.
from .models import Order, OrderItems

admin.site.register(Order)
admin.site.register(OrderItems)