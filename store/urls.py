from django.urls import path
from . import views
urlpatterns = [path('products/', views.products, name="store-products"),
    path('products/<id>/', views.product_detail, name='store-product_detail'),
    path('collections/<pk>/', views.collection_detail, name='store-collection-detail'),
    path('collections/', views.CollectionView.as_view(), name='store-collections'),
    path('customers/', views.CustomerMixin.as_view(), name='store-customers'),
    path('carts/', views.CartView.as_view(), name='store-carts'),
    path('carts/<pk>/', views.CartDetailView.as_view(), name='store-cart-detail'),
    path('carts/<cart_pk>/items/', views.CartItemView.as_view(), name='store-cart-detail'),

]