from django.urls import path
from . import views
urlpatterns = [path('products/', views.products, name="store-products"),
    path('products/<id>/', views.product_detail, name='store-product_detail'),
]