from __future__ import unicode_literals
from django.contrib import admin

from pis_product.models import Product
from pis_product.models import ProductDetail
from pis_product.models import PurchasedProduct
from pis_product.models import ExtraItems
from pis_product.models import ClaimedProduct
from pis_product.models import StockIn,StockOut


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'brand_name','UNIT_TYPE_QUANTITY', 'retailer',
        'quantity', 'retail_price', 'consumer_price','bar_code'
    )
    search_fields = (
        'name', 'brand_name', 'retailer__name','bar_code','unit_type'
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
        '__unicode__', 'retailer', 'invoice_no', 'discount_percentage', 'created_at'
    )

    search_fields = ('product__name', 'product__retailer__name')
    raw_id_fields = ('product',)

    @staticmethod
    def retailer(obj):
        return obj.product.retailer.name

    @staticmethod
    def invoice_no(obj):
        return obj.invoice.receipt_no if obj.invoice else ''


class ExtraItemsAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'retailer', 'quantity', 'price', 'discount_percentage',
        'total')

    search_fields = ('item_name', 'retailer__name')
    raw_id_fields = ('retailer', )

    @staticmethod
    def retailer(obj):
        return obj.product.retailer.item_name


class ClaimedProductAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'brand_name', 'customer', 'claimed_items',
        'claimed_amount', 'created_at'
    )
    search_fields = ('product__name', 'product__brand_name')
    raw_id_fields = ('product',)

    @staticmethod
    def brand_name(obj):
        return obj.product.brand_name or None

    @staticmethod
    def customer(obj):
        return obj.customer.customer_name or None


class StockInAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'product', 'quantity', 'price_per_item',
        'total_amount', 'dated_order','stock_expiry'
    )
    search_fields = ('product__name','stock_expiry','dated_order')


class StockOutAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'product', 'invoice_no', 'stock_out_quantity', 'dated',
    )
    search_fields = ('product__name','stock_out_quantity','dated')

    @staticmethod
    def invoice_no(obj):
        return obj.invoice.receipt_no if obj.invoice else ''


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(PurchasedProduct, PurchasedProductAdmin)
admin.site.register(ExtraItems, ExtraItemsAdmin)
admin.site.register(ClaimedProduct, ClaimedProductAdmin)
admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
