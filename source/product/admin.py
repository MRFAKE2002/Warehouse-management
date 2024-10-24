from django.contrib import admin
from .models import Variant, Supply, Category, Type, Size


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):

    list_display = ('id', 'image_tag','title', 'status', 'category_to_str', 'type_to_str', 'size_to_str')
    list_filter = (['id', 'status'])
    search_fields = ('id', 'title')
    ordering = ['id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'title')
    list_filter = (['id', 'title'])
    search_fields = ('id', 'title')
    ordering = ['id']

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display=('supply', 'type', 'size', 'inventory', 'price_buy', 'price')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):

    list_display=('name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display=('name',)
