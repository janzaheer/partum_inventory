from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum

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

    def product_available_items(self):
        obj = self.product_detail.aggregate(Sum('available_item'))
        return obj.get('available_item__sum')

    def product_purchased_items(self):
        obj = self.product_detail.aggregate(Sum('purchased_item'))
        return obj.get('purchased_item__sum')


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
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, default=1, blank=True, null=True
    )
    discount_percentage = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )
    purchase_amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )

    def __unicode__(self):
        return self.product.name


class ExtraItems(DatedModel):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer', related_name='retailer_extra_items'
    )
    item_name = models.CharField(
        max_length=100, blank=True, null=True)
    quantity = models.CharField(
        max_length=100, blank=True, null=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True)
    total = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True)

    def __unicode__(self):
        return self.item_name


# Signals
def purchase_product(sender, instance, created, **kwargs):
    """
    TODO: Zaheer Please check this function is useful or not.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    product_items = (
        instance.product.product_detail.filter(
            available_item__gt=0).order_by('created_at')
    )

    if product_items:
        item = product_items[0]
        item.available_item - 1
        item.save()
