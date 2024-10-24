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
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=datetime.datetime(2024, 6, 2, 9, 0, 19, 516717, tzinfo=datetime.timezone.utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to=settings.AUTH_USER_MODEL, verbose_name=' نام کاربر')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': ' سبد خرید',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='تعداد محصول')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cart', verbose_name=' سبد خرید')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cart_supply', to='product.variant', unique=True, verbose_name='نام محصول')),
            ],
            options={
                'verbose_name': 'اقلام سبد خرید',
                'verbose_name_plural': ' اقلام سبد خرید',
            },
        ),
    ]