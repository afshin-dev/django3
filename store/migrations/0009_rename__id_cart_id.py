# Generated by Django 3.2 on 2022-04-19 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_cartitem_cartiitem_cart_product_unique'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='_id',
            new_name='id',
        ),
    ]
