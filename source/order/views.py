from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from product.models import Variant
from django.contrib import messages
from django.http import HttpResponseRedirect
import jdatetime

from .filters import OrderFilter

def order_detail(request):
    orders = Order.objects.prefetch_related('order_items').all()
    
    context = {
        'orders':orders,
    }
    
    return render(request, 'order/order_list.html', context)


@require_POST
def order_create(request):
    try:
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        
        cart = Cart.objects.get(user_id=request.user.id)
        
        cart_items = CartItem.objects.filter(cart_id = cart)
        
        order = Order.objects.create(user_id=request.user.id, customer_name=customer_name, customer_phone_number=customer_phone, is_paid=True)
        
        for item in cart_items:
            OrderItem.objects.create(order_id=order.id, variant=item.variant, price_buy=item.variant.price_buy, price=item.variant.price, quantity=item.quantity)
            variant = Variant.objects.get(id= item.variant.id)
            variant.inventory -= item.quantity
            variant.save()
        
        Cart.objects.filter(user_id=request.user.id).delete()
        messages.success(request, "سفارش شما با موفقیت ساخته شد.")

        return redirect('order:order_detail')
    except:
        messages.warning(request, "در ابتدا باید محصول مورد نظر را به سبد خرید اضافه کنید.")
        return redirect('product:variant_list')


def remove_order_item(request, order_id, order_item_id):

    url = request.META.get('HTTP_REFERER')    
    order_user = Order.objects.get(id=order_id, user__id=request.user.id)
    order_item = OrderItem.objects.get(id=order_item_id, order__id=order_user.id)

    order_item.delete()
    messages.success(request, "مورد مدنظر از سفارش شما با موفقیت حذف شد.")
    
    order = Order.objects.get(id=order_id, user__id=request.user.id)
    if order.order_items.count() == 0:
        order.delete()

    return HttpResponseRedirect(url)


def clear_order(request, order_id):  
    url = request.META.get('HTTP_REFERER')
    order = Order.objects.get(id=order_id, user__id=request.user.id)
    order.delete()
    messages.success(request, "سفارش شما با موفقیت پاک شد.")

    return HttpResponseRedirect(url)


#---------------------------------------------------------------------------------

# def order_filter_list(request):
#     orders = Order.objects.prefetch_related('order_items').all()
    
#     if request.method == 'POST':
#         form = OrderFilter(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data.get('start_date')
#             end_date = form.cleaned_data.get('end_date')
#             if start_date and end_date:
#                 orders = orders.filter(create_at__range=[start_date, end_date])
#     else:
#         form = OrderFilter()
    
#     context = {
#         'orders': orders,
#         'form': form,
#     }
    
#     return render(request, 'order/order_filter_list.html', context)

def order_filter_list(request):
    orders = Order.objects.prefetch_related('order_items').all()
    
    form = OrderFilter(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        start_date_jalali = form.cleaned_data.get('start_date')
        end_date_jalali = form.cleaned_data.get('end_date')

        if start_date_jalali and end_date_jalali:
            start_date_str = start_date_jalali.strftime('%Y-%m-%d')
            end_date_str = end_date_jalali.strftime('%Y-%m-%d')
            
            start_date_gregorian = jdatetime.datetime.strptime(start_date_str, '%Y-%m-%d').togregorian()
            end_date_gregorian = jdatetime.datetime.strptime(end_date_str, '%Y-%m-%d').togregorian()
            
            orders = orders.filter(create_at__range=[start_date_gregorian, end_date_gregorian])
    
    context = {
        'orders': orders,
        'form': form,
    }

    return render(request, 'order/order_filter_list.html', context)