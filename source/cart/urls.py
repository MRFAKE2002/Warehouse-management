from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add', views.add_cart, name='add'),
    path('remove/<int:cart_item_id>', views.remove_cart, name='remove'),
    path('clear', views.clear_cart, name='clear'),
]
