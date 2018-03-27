from __future__ import unicode_literals
from django.contrib import admin

from pis_product.models import Product
from pis_product.models import ProductDetail
from pis_product.models import PurchasedProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'brand_name', 'retailer',
        'quantity', 'retail_price', 'consumer_price'
    )
    search_fields = (
        'name', 'brand_name', 'retailer__name'
    )
    raw_id_fields = ('retailer',)

    @staticmethod
    def retailer(obj):
        return obj.retailer.name

    @staticmethod
    def quantity(obj):
        return 'under progress'

    @staticmethod
    def retail_price(obj):
        return 'under progress'

    @staticmethod
    def consumer_price(obj):
        return 'under progress'


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'brand_name', 'retailer', 'retail_price',
        'consumer_price', 'discount_amount', 'profit_amount',
        'available_item', 'purchased_item', 'remaining_item'
    )

    search_fields = (
        'product__name', 'product__retailer__name', 'product__brand_name'
    )

    raw_id_fields = ('product',)

    @staticmethod
    def retailer(obj):
        return obj.product.retailer.name

    @staticmethod
    def brand_name(obj):
        return obj.product.brand_name

    @staticmethod
    def discount_amount(obj):
        return 'under_progress'

    @staticmethod
    def profit_amount(obj):
        return obj.consumer_price - obj.retail_price

    @staticmethod
    def remaining_item(obj):
        return obj.available_item - obj.purchased_item


class PurchasedProductAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'retailer', 'discount', 'created_at'
    )

    search_fields = ('product__name', 'product__retailer__name')
    raw_id_fields = ('product',)

    @staticmethod
    def retailer(obj):
        return obj.product.retailer.name

    @staticmethod
    def discount(obj):
        return obj.manual_discount + obj.discount_percentage


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(PurchasedProduct, PurchasedProductAdmin)
