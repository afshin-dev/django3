# Generated by Django 3.2 on 2022-04-20 14:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=40, max_digits=6, validators=[django.core.validators.MinValueValidator(0.001)]),
            preserve_default=False,
        ),
    ]
