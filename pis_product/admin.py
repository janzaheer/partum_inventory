from django.contrib import admin

from pis_product.models import Product, ProductDetail, PurchasedProduct
from pis_product.models import ExtraItems, ClaimedProduct, StockIn, StockOut


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'brand_name', 'unit_type', 'retailer_name', 'bar_code',
    )
    search_fields = (
        'name', 'brand_name', 'retailer__name', 'bar_code', 'unit_type',
    )
    raw_id_fields = ('retailer',)
    list_filter = ('unit_type', 'retailer')

    @admin.display(description='Retailer')
    def retailer_name(self, obj):
        return obj.retailer.name


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'brand_name', 'retailer_name', 'retail_price',
        'consumer_price', 'profit_amount',
        'available_item', 'purchased_item', 'remaining_item',
    )
    search_fields = (
        'product__name', 'product__retailer__name', 'product__brand_name',
    )
    raw_id_fields = ('product',)

    @admin.display(description='Retailer')
    def retailer_name(self, obj):
        return obj.product.retailer.name

    @admin.display(description='Brand')
    def brand_name(self, obj):
        return obj.product.brand_name

    @admin.display(description='Profit')
    def profit_amount(self, obj):
        return obj.consumer_price - obj.retail_price

    @admin.display(description='Remaining')
    def remaining_item(self, obj):
        return obj.available_item - obj.purchased_item


class PurchasedProductAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'retailer_name', 'invoice_no', 'discount_percentage', 'created_at',
    )
    search_fields = ('product__name', 'product__retailer__name')
    raw_id_fields = ('product',)

    @admin.display(description='Retailer')
    def retailer_name(self, obj):
        return obj.product.retailer.name

    @admin.display(description='Invoice #')
    def invoice_no(self, obj):
        return obj.invoice.receipt_no if obj.invoice else ''


class ExtraItemsAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'retailer_name', 'quantity', 'price', 'discount_percentage',
        'total',
    )
    search_fields = ('item_name', 'retailer__name')
    raw_id_fields = ('retailer',)

    @admin.display(description='Retailer')
    def retailer_name(self, obj):
        return obj.retailer.name


class ClaimedProductAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'brand_name', 'customer_name', 'claimed_items',
        'claimed_amount', 'created_at',
    )
    search_fields = ('product__name', 'product__brand_name')
    raw_id_fields = ('product',)

    @admin.display(description='Brand')
    def brand_name(self, obj):
        return obj.product.brand_name or None

    @admin.display(description='Customer')
    def customer_name(self, obj):
        return obj.customer.customer_name if obj.customer else None


class StockInAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'product', 'quantity', 'price_per_item',
        'total_amount', 'dated_order', 'stock_expiry',
    )
    search_fields = ('product__name',)
    list_filter = ('dated_order',)


class StockOutAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'product', 'invoice_no', 'stock_out_quantity', 'dated',
    )
    search_fields = ('product__name',)
    list_filter = ('dated',)

    @admin.display(description='Invoice #')
    def invoice_no(self, obj):
        return obj.invoice.receipt_no if obj.invoice else ''


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(PurchasedProduct, PurchasedProductAdmin)
admin.site.register(ExtraItems, ExtraItemsAdmin)
admin.site.register(ClaimedProduct, ClaimedProductAdmin)
admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
