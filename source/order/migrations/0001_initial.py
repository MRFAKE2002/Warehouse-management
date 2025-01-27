# Generated by Django 5.0.3 on 2024-06-02 09:00

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=datetime.datetime(2024, 6, 2, 9, 0, 19, 519636, tzinfo=datetime.timezone.utc))),
                ('customer_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم مشتری')),
                ('customer_phone_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='شماره مشتری')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت انجام شد؟')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL, verbose_name=' نام کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': ' سفارشات',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_buy', models.PositiveIntegerField(verbose_name='قیمت خرید محصول')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت فروش محصول')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='تعداد محصول')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order', verbose_name=' سفارش')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_variants', to='product.variant', verbose_name='نام محصول')),
            ],
            options={
                'verbose_name': 'اقلام سفارش',
                'verbose_name_plural': ' اقلام سفارشات',
            },
        ),
    ]
