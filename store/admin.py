from typing import List, Tuple, Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Product, Collection, Customer, Order
from django.db.models import Count
from django.utils.html import format_html
from django.contrib import messages
# Register your models here.


class PriceFilter(admin.SimpleListFilter):
    title = 'Income average of society'
    parameter_name = 'cost'

    def lookups(self, request, model_admin) -> List[Tuple[Any, str]]:
        return [('cheap', 'Cheap'), ('suitable', 'Suitable'), ('high', 'High')]

    def queryset(self, request: Any, queryset):
        if self.value() == 'cheap':
            return queryset.filter(price__lt=1000)
        if self.value() == 'suitable':
            return queryset.filter(price__lt=5000)
        if self.value() == 'high':
            return queryset.filter(price__gt=5000)


class ProductAdmin(admin.ModelAdmin):
    actions = ['reset_inventory']
    prepopulated_fields = {
        'slug' : ['title']
    }
    list_display = [
        'title',
        'price',
        'inventory',
        'inventory_status',
        'collections',
    ]
    list_editable = ['price']
    search_fields = ['title']
    list_filter = ['collections', PriceFilter]

    def inventory_status(self, product) -> str:
        return 'low' if product.inventory < 10 else 'ok'

    @admin.action(description='reset inventory (to zero)')
    def reset_inventory(self, request, queryset):
        count = queryset.update(inventory=0)
        self.message_user(request,
                          f'successfuly reset {count} product inventory',
                          level=messages.SUCCESS)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'featured_product', 'product_count']

    def product_count(self, collection):
        return format_html(
            '<a href="http://google.com" target="_blank" >{}</a>',
            collection.product_count)

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            product_count=Count('product'))


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'email']
    list_editable = ['membership']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'payment_status', 'customer']
    list_select_related = ['customer']


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)