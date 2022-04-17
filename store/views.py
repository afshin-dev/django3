from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import connection
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
# Create your views here.


@api_view()  # for
def products(request: Request):
    return Response([
        f'{product.id} - {product.title}'
        for product in Product.objects.all().order_by('id')
    ])


@api_view()
def product_detail(request: Request, id: str) -> Response:
    print(id)
    return Response(id)