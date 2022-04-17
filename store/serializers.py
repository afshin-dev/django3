from rest_framework import serializers

from store.models import Product, Collection
from decimal import Decimal


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255, trim_whitespace=True)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255, trim_whitespace=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    with_tax = serializers.SerializerMethodField(method_name='calc_tax')
    description = serializers.CharField(max_length=1023, trim_whitespace=True)
    inventory = serializers.IntegerField()
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all(),
    #     source='collection_id'
    #     )
    collection = CollectionSerializer()

    def calc_tax(self, p: Product):
        return p.price * Decimal('1.1')