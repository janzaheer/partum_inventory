from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum
import random
from django.db.models.signals import post_save

from pis_com.models import DatedModel


class Product(models.Model):
    UNIT_TYPE_KG = 'Kilogram'
    UNIT_TYPE_GRAM = 'Gram'
    UNIT_TYPE_LITRE = 'Litre'
    UNIT_TYPE_QUANTITY = 'Quantity'

    UNIT_TYPES = (
        (UNIT_TYPE_KG, 'Kilogram'),
        (UNIT_TYPE_GRAM, 'Gram'),
        (UNIT_TYPE_LITRE, 'Litre'),
        (UNIT_TYPE_QUANTITY, 'Quantity'),
    )
    unit_type = models.CharField(
        choices=UNIT_TYPES, default=UNIT_TYPE_QUANTITY,
        blank=True, null=True, max_length=200
    )
    name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=200)
    retailer = models.ForeignKey(
        'pis_retailer.Retailer',
        related_name='retailer_product'
    )
    bar_code = models.CharField(max_length=13, unique=True, blank=True,
                                null=True)

    def __unicode__(self):
        return self.name

    def total_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum('quantity'))
            stock_in = float(obj_stock_in.get('quantity__sum'))
        except:
            stock_in = 0

        return stock_in


    def product_available_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum('quantity'))
            stock_in = float(obj_stock_in.get('quantity__sum'))
        except:
            stock_in = 0

        try:
            obj_stock_out = self.stockout_product.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0
        return  stock_in - stock_out

    def product_purchased_items(self):
        try:
            obj_stock_out = self.stockout_product.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0
        return  stock_out

    def total_num_of_claimed_items(self):
        obj = self.claimed_product.aggregate(Sum('claimed_items'))
        return obj.get('claimed_items__sum')

# Signals Function for bar code
def create_save_bar_code(sender, instance, created, **kwargs):
    if created and not instance.bar_code:
        while True:
            random_bar_code = random.randint(1000000000000, 9999999999999)
            if (
                not Product.objects.filter(bar_code=random_bar_code).exists()
            ):
                break

        instance.bar_code = random_bar_code
        instance.save()

# Signal Calls bar code
post_save.connect(create_save_bar_code, sender=Product)



class StockIn(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockin_product'
    )
    quantity=models.CharField(
        max_length=100, blank=True, null=True
    )
    price_per_item=models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    total_amount=models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    dated_order=models.DateField(blank=True, null=True)
    stock_expiry=models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.product.name

class StockOut(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockout_product'
    )
    stock_out_quantity=models.CharField(max_length=100, blank=True, null=True)
    dated=models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.product.name




class ProductDetail(DatedModel):
    product = models.ForeignKey(
        Product, related_name='product_detail'
    )
    retail_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0
    )
    consumer_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0
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
        max_digits=65, decimal_places=2, default=1, blank=True, null=True
    )
    price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    discount_percentage = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    purchase_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
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
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)
    total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)

    def __unicode__(self):
        return self.item_name or ''


class ClaimedProduct(DatedModel):
    product = models.ForeignKey(Product, related_name='claimed_product')
    customer = models.ForeignKey(
        'pis_com.Customer', related_name='customer_claimed_items',
        null=True, blank=True,
    )
    claimed_items = models.IntegerField(
        default=1, verbose_name='No. of Claimed Items')
    claimed_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)

    def __unicode__(self):
        return self.product.name


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
