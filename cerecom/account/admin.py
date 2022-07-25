from django.contrib import admin
from django.contrib.admin import ModelAdmin


# Register your models here.
from .models import UserBase

@admin.register(UserBase)
class  UserBaseAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']