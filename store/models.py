from operator import mod
from turtle import title
from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255, unique=True, null=False)
    featured_product = models.ForeignKey('Product',
                                         on_delete=models.SET_NULL,
                                         null=True)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.001)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collections = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title


class Customer(models.Model):
    # outside_interface = [first_name, last_name, birth_date, membership]
    MEMBERSHIP_CHOICES = [
        ('B', 'Bronze'),  # tuple 
        ('S', 'Silver'),  # tuple 
        ('G', 'Gold')  # tuple 
    ]
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=1,
                                  choices=MEMBERSHIP_CHOICES,
                                  default='B')


class Order(models.Model):
    PAYMENT_STATUS = [('P', 'PENDING'), ('C', 'COMPLETE'), ('F', 'FAILED')]
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,
                                      choices=PAYMENT_STATUS,
                                      default='P')
    customer = models.ForeignKey(Product, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'],name="cartiitem_cart_product_unique")
        ]

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=100, null=True)