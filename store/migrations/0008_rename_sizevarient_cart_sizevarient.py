# Generated by Django 4.1.7 on 2023-03-15 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_size_cart_sizevarient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='SizeVarient',
            new_name='sizeVarient',
        ),
    ]
