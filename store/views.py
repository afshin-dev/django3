from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import connection

# Create your views here.
def index(request:HttpRequest):
    return HttpResponse("this is index page of store app")