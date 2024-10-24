from django.contrib import admin
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin	

class OrderItemInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = OrderItem
    list_display = ['order', 'variant', 'size', 'type', 'price', 'quantity', 'total_price']


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['id', 'user', 'customer_name', 'customer_phone_number', 'create_at', 'get_total_price']
    list_filter = ['create_at']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'variant', 'size', 'type', 'price', 'quantity', 'total_price']

