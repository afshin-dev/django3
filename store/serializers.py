from ast import Raise
from importlib.resources import contents
from turtle import title
from django.forms import ValidationError
from rest_framework import serializers

from store.models import CartItem, Customer, Product, Collection, Cart
from decimal import Decimal
from django.utils.text import slugify


class InventoryNotEnoughException(Exception):
    pass


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
    slug = serializers.SlugField(read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    with_tax = serializers.SerializerMethodField(method_name='calc_tax')
    description = serializers.CharField(max_length=1023, trim_whitespace=True)
    inventory = serializers.IntegerField()
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all(),
    #     source='collection_id'
    #     )
    collections = CollectionSerializer()
    collection_detail = serializers.HyperlinkedRelatedField(
        source='collections',
        queryset=Collection.objects.all(),
        view_name='store-collection-detail',
    )

    def calc_tax(self, p: Product):
        return p.price * Decimal('1.1')

    def validate_title(self, value: str):
        product = Product.objects.filter(title=value).exists()
        if product:
            raise serializers.ValidationError("product already exist")
        return value


class CreateProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, trim_whitespace=True)
    slug = serializers.SlugField(read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    description = serializers.CharField(max_length=1023, trim_whitespace=True)
    inventory = serializers.IntegerField()
    collections = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all())

    def create(self, validated_data):
        product = Product()
        product.title = validated_data['title']
        product.price = validated_data['price']
        product.description = validated_data['description']
        product.inventory = validated_data['inventory']
        product.collections = validated_data['collections']
        product.slug = slugify(product.title)
        product.save()

        print("product with id", product.id, "created")

        new_ser = ProductSerializer(
            product, context={'request': self.context['request']})
        return new_ser.data
        # return Product.objects.create(title=product.title,
        #                               price=product.price,
        #                               description=product.description,
        #                               inventory=product.inventory,
        #                               collections=product.collections,
        #                               slug=product.slug)

    # update responsible to put action or (update all nesseccary field)
    def update(self, instance: Product, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.inventory = validated_data.get('inventory',
                                                instance.inventory)
        instance.collections = validated_data.get('collections',
                                                  instance.collections)
        instance.slug = slugify(validated_data.get('title', instance.title))
        instance.save()

        new_ser = ProductSerializer(
            instance, context={'request': self.context['request']})
        return new_ser.data


class PatchProductSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=1023, required=False)
    inventory = serializers.IntegerField(required=False)

    def update(self, instance: Product, validated_data):
        if len(validated_data.keys()) == 0:
            ser = ProductSerializer(
                instance, context={'request': self.context['request']})
            return ser.data
        instance.inventory = validated_data.get('inventory',
                                                instance.inventory)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.save()

        ser = ProductSerializer(instance,
                                context={'request': self.context['request']})
        return ser.data


class CustomerSerializer(serializers.Serializer):
    MEMBERSHIP_CHOICES = [
        ('B', 'Bronze'),  # tuple 
        ('S', 'Silver'),  # tuple 
        ('G', 'Gold')  # tuple 
    ]
    first_name = serializers.CharField(max_length=255, trim_whitespace=True)
    last_name = serializers.CharField(max_length=255, trim_whitespace=True)
    birth_date = serializers.DateField()
    membership = serializers.ChoiceField(choices=MEMBERSHIP_CHOICES,
                                         default='B')

    def create(self, validated_data):
        new_Customer = Customer()
        new_Customer.first_name = validated_data['first_name']
        new_Customer.last_name = validated_data['last_name']
        new_Customer.birth_date = validated_data['birth_date']
        new_Customer.membership = validated_data['membership']
        new_Customer.email = "ap@oi.com"
        new_Customer.save()
        return new_Customer


class SimpleCartItemSerializer(serializers.Serializer):
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    quantity = serializers.IntegerField(min_value=0)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_price = serializers.SerializerMethodField(
        method_name='calc_total_price')

    def calc_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.price


class CreateCartItemSerializer(serializers.Serializer):
    cart = serializers.UUIDField()
    product = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)

    def validate_cart(self, value):
        is_cart_exists = Cart.objects.filter(id=value).exists()
        if is_cart_exists is False:
            raise serializers.ValidationError("cart does not exists")
        return value

    def validate_product(self, value: int):
        is_product_exists = Product.objects.filter(id=value).exists()
        if is_product_exists is False:
            raise serializers.ValidationError("product does not exists")
        return value

    def create(self, validated_data):
        product: Product = Product.objects.get(
            id=validated_data['product'])  # if this line failed there is wrong
        # somewhere (technically at this stage must not error happen)

        if product.inventory < validated_data['quantity']:
            raise InventoryNotEnoughException(
                "our inventory less than your request quantity")

        if CartItem.objects.filter(cart=validated_data['cart'],
                                   product=validated_data['product']).exists():
            cart_item: CartItem = CartItem.objects.filter(
                cart=validated_data['cart'], product=validated_data['product']).first()
            cart_item.quantity += validated_data['quantity']
            cart_item.save()
            serializer = SimpleCartItemSerializer(cart_item)
            return serializer.data
        # create new item in cartitem
        new_cart_item = CartItem()
        new_cart_item.product_id = validated_data['product']
        new_cart_item.cart_id = validated_data['cart']
        new_cart_item.quantity = validated_data['quantity']
        new_cart_item.price = product.price
        new_cart_item.save()

        new_cart_item_serializer = SimpleCartItemSerializer(new_cart_item)
        return new_cart_item_serializer.data 


class CartSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    items = SimpleCartItemSerializer(many=True)