from django import template
from pis_product.models import StockIn,StockOut, Product

register = template.Library()

@register.simple_tag
def product_notifications(retailer_id):
    return Product.objects.filter(retailer__id=retailer_id)
