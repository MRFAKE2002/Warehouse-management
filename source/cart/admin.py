from django.contrib import admin
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin	

class CartItemInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = CartItem
    list_display = ['cart', 'variant', 'size', 'type', 'price', 'quantity', 'total_price']


@admin.register(Cart)
class CartAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['user', 'create_at', 'get_total_price']
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'variant', 'size', 'type', 'price', 'quantity', 'total_price']

