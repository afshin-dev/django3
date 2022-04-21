from multiprocessing import context
from os import stat
from urllib import response
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import connection
from .models import CartItem, Product, Collection, Customer, Cart
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import CreateCartItemSerializer, CustomerSerializer, CreateCollectionSerializer, ProductSerializer, CollectionSerializer, CreateCollectionSerializer, CreateProductSerializer, PatchProductSerializer, CartSerializer, SimpleCartItemSerializer
from rest_framework import status
from django.db.models.aggregates import Count
from store import serializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
# Create your views here.


class CollectionView(APIView):

    def get(self, request: Request) -> Response:
        collections = Collection.objects.all().only('id', 'title')
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializers = CreateCollectionSerializer(data=request.data)
        if serializers.is_valid():
            new_collection = serializers.create(serializers.validated_data)
            response_serializer = CollectionSerializer(
                new_collection)  # serialize new collection for outside api

            return Response(response_serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors,
                            status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view()
def collection_detail(request: Request, pk: str) -> Response:
    collection = None
    try:
        collection = Collection.objects.get(pk=int(pk))
    except Collection.DoesNotExist:
        return Response('{"error": "collection not found"}',
                        status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response('{"error": "invalid id"}',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])  # for
def products(request: Request):
    if request.method == 'GET':

        products = Product.objects.all()
        serializer = ProductSerializer(products,
                                       many=True,
                                       context={'request': request})

        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CreateProductSerializer(data=request.data,
                                             context={"request": request})
        if serializer.is_valid():
            new_product = serializer.save()
            # new_ser = ProductSerializer(new_product, context={'request': request})
            return Response(new_product, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def product_detail(request: Request, id: str) -> Response:
    product = None
    try:
        product = Product.objects.get(pk=int(id))
    except Product.DoesNotExist:
        return Response('{"error": "product not found"}',
                        status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response('{"error": "invalid id"}',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        product.delete()
        return Response('', status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        serializer = CreateProductSerializer(product,
                                             data=request.data,
                                             context={'request': request})
        if serializer.is_valid():
            updated_product = serializer.save()
            return Response(updated_product, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        ser = PatchProductSerializer(product,
                                     data=request.data,
                                     context={'request': request})
        if ser.is_valid():
            patched_product = ser.save()
            return Response(patched_product, status=status.HTTP_202_ACCEPTED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerMixin(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)

    def post(self, request):
        return self.create(request)


class CartView(APIView):

    def get(self, request: Request) -> Response:
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        cart = Cart()
        cart.save()
        return Response(cart.id, status=status.HTTP_201_CREATED)


class CartDetailView(APIView):

    def get(self, request, pk):
        cart = None
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            Response('cart not found', status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemView(APIView):

    def get(self, request: Request, cart_pk) -> Response:
        cart_items = CartItem.objects.filter(cart=cart_pk)
        serializer = SimpleCartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request, cart_pk) -> Response:
        # {cart : uuid , product : int , quantity : int }

        # check for existance of cart
        # check for existance of product
        # check for enogh product in inventory
        # check for item already exists or not

        serializer = CreateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
                            
        cart_item = serializer.save()
        return Response(cart_item, status=status.HTTP_201_CREATED)
