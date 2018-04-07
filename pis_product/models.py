from __future__ import unicode_literals
from django.db import models

from pis_com.models import DatedModel


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=200)
    retailer = models.ForeignKey(
        'pis_retailer.Retailer',
        related_name='retailer_product'
    )

    def __unicode__(self):
        return self.name


class ProductDetail(DatedModel):
    product = models.ForeignKey(
        Product, related_name='product_detail'
    )
    retail_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    consumer_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    available_item = models.IntegerField(default=1)
    purchased_item = models.IntegerField(default=0)

    def __unicode__(self):
        return self.product.name


class PurchasedProduct(DatedModel):
    product = models.ForeignKey(
        Product, related_name='purchased_product'
    )
    manual_discount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    discount_percentage = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    purchase_amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )

    def __unicode__(self):
        return self.product.name
