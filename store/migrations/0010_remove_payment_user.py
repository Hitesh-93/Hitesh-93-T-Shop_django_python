# Generated by Django 4.1.7 on 2023-03-21 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_order_payment_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
    ]