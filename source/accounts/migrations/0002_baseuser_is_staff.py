# Generated by Django 5.0.3 on 2024-04-26 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]