# Generated by Django 3.2 on 2022-04-20 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default='dd1c8760-477b-4107-b8c5-c4b39254b80a', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.cart'),
            preserve_default=False,
        ),
    ]
