from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('remove/<int:order_id>/<int:order_item_id>/', views.remove_order_item, name='remove'),
    path('clear/<int:order_id>/', views.clear_order, name='clear'),
    path('order-filter/', views.order_filter_list, name='order_filter'),
]
