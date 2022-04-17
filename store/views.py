from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import connection
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework import status
# Create your views here.


@api_view()  # for
def products(request: Request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    
    return Response(serializer.data)


@api_view()
def product_detail(request: Request, id: str) -> Response:
    product = None
    try:
        product = Product.objects.get(pk=int(id))
    except Product.DoesNotExist:
        return Response('{"error": "product not found"}',status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response('{"error": "invalid id"}',status=status.HTTP_406_NOT_ACCEPTABLE)    
    serializer = ProductSerializer(product)
    return Response(serializer.data,status=status.HTTP_200_OK )    