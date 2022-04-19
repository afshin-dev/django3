from turtle import title
from rest_framework import serializers

from store.models import Customer, Product, Collection
from decimal import Decimal

#outside interface of collection
class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255, trim_whitespace=True)

# form of saving collection
class CreateCollectionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, trim_whitespace=True)

    def create(self, validated_data):
        return Collection.objects.create(title=validated_data['title'])

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
    collections = CollectionSerializer()
    collection_detail =serializers.HyperlinkedRelatedField(source='collections',
    queryset = Collection.objects.all(),
    view_name='store-collection-detail'
    )

    def calc_tax(self, p: Product):
        return p.price * Decimal('1.1')

class CustomerSerializer(serializers.Serializer):
    MEMBERSHIP_CHOICES = [
        ('B', 'Bronze'),  # tuple 
        ('S', 'Silver'),  # tuple 
        ('G', 'Gold')  # tuple 
    ]
    first_name = serializers.CharField(max_length=255, trim_whitespace=True)
    last_name = serializers.CharField(max_length=255, trim_whitespace=True)
    birth_date = serializers.DateField()
    membership = serializers.ChoiceField(choices=MEMBERSHIP_CHOICES, default='B')

    def create(self, validated_data):
        new_Customer = Customer()
        new_Customer.first_name = validated_data['first_name']
        new_Customer.last_name = validated_data['last_name']
        new_Customer.birth_date = validated_data['birth_date']
        new_Customer.membership = validated_data['membership']
        new_Customer.email = "ap@oi.com"
        new_Customer.save()
        return new_Customer

