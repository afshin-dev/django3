from urllib import response
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import connection
from .models import Product, Collection
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import CreateCollectionSerializer, ProductSerializer, CollectionSerializer, CreateCollectionSerializer
from rest_framework import status
from django.db.models.aggregates import Count
from store import serializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin,UpdateModelMixin
# Create your views here.



class CollectionView(APIView):

    def get(self, request: Request) -> Response:
        collections = Collection.objects.all().only('id', 'title')
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializers = CreateCollectionSerializer(data= request.data)
        if serializers.is_valid():
            new_collection = serializers.create(serializers.validated_data)
            response_serializer = CollectionSerializer(new_collection) # serialize new collection for outside api

            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            


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


@api_view()  # for
def products(request: Request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,
                                   many=True,
                                   context={'request': request})

    return Response(serializer.data)


@api_view()
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
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
