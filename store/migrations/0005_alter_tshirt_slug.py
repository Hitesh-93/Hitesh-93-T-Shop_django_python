# Generated by Django 4.1.7 on 2023-03-02 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_tshirt_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tshirt',
            name='slug',
            field=models.CharField(default='', max_length=200, null=True, unique=True),
        ),
    ]