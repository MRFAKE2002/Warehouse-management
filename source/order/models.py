from django.db import models
from product.models import Variant
from accounts.models import BaseUser
from django.utils import timezone

class Order(models.Model):

    user = models.ForeignKey(BaseUser, verbose_name=' نام کاربر', on_delete=models.CASCADE, related_name='order_user')
    create_at = models.DateTimeField(default=timezone.now())
    customer_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='اسم مشتری')
    customer_phone_number = models.CharField(max_length=12, blank=True, null=True, verbose_name='شماره مشتری')
    get_total_price = models.PositiveIntegerField(verbose_name='قیمت سفارش')
    is_paid = models.BooleanField(verbose_name='پرداخت انجام شد؟', default=False)

    def __str__(self):
        return f'کاربر:{self.user.username} | شماره سفارش: {self.id}'

    @property
    def get_total_price(self):
        return sum(i.total_price() for i in self.order_items.all())

    class Meta:
    
        verbose_name = 'سفارش'
        verbose_name_plural = ' سفارشات'


class OrderItem(models.Model):

    order = models.ForeignKey(Order, verbose_name=' سفارش', on_delete=models.CASCADE, related_name='order_items')
    variant =  models.ForeignKey(Variant, verbose_name='نام محصول', on_delete=models.PROTECT, related_name='order_variants')
    price_buy = models.PositiveIntegerField(verbose_name='قیمت خرید محصول')
    price = models.PositiveIntegerField(verbose_name='قیمت فروش محصول')
    quantity = models.PositiveIntegerField(verbose_name='تعداد محصول', default=1)

    def __str__(self):
        return f'کاربر:{self.order.user.username} | شماره سفارش: {self.order.id}'
    

    def size(self):
        try:
            return self.variant.size.name
        except:
            return 'هیچی'

    def type(self):
        try:
            return self.variant.type.name
        except:
            return 'هیچی'

    def total_purchase_profit(self):
        return (self.price - self.price_buy) * self.quantity

    def total_price(self):
        return self.price * self.quantity

    class Meta:
    
        verbose_name = 'اقلام سفارش'
        verbose_name_plural = ' اقلام سفارشات'
