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
    name = models.CharField(max_length=100, unique=True)
    brand_name = models.CharField(max_length=200, blank=True, null=True)
    retailer = models.ForeignKey(
        'pis_retailer.Retailer',
        related_name='retailer_product',on_delete=models.CASCADE
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


def int_to_bin(value):
        return bin(value)[2:]


def bin_to_int(value):
        return int(value, base=2)


# Signals Function for bar code
def create_save_bar_code(sender, instance, created, **kwargs):

    if not instance.bar_code:
        import time
        from pis_com import ean13

        code = None

        r = random.Random(time.time())
        m = int_to_bin(instance.pk % 4)
        if len(m) == 1:
            m = '0' + m
        elif not len(m):
            m = '00'

        while not code:
            g = ''.join([str(r.randint(0, 1)) for i in range(32)])
            chk = int_to_bin(bin_to_int(g) % 16)

            if len(chk) < 4:
                chk = '0' * (4 - len(chk)) + chk

            chk = ''.join(['1' if x == '0' else '0' for x in chk])

            if m == '11':
                code = ''.join(['1', m, g[:16], chk, g[16:32]])
            elif m == '10':
                code = ''.join(['1', m, g[:11], chk, g[11:32]])
            elif m == '01':
                code = ''.join(['1', m, g[:19], chk, g[19:32]])
            else:
                code = ''.join(
                    ['1', m, g[:9], chk[:2], g[9:23], chk[2:4], g[23:32]])

            code = '%d' % bin_to_int(code)
            code += '%d' % ean13.get_checksum(code)

        instance.bar_code = code
        instance.save()


# Signal Calls bar code
post_save.connect(create_save_bar_code, sender=Product)


class StockIn(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockin_product',on_delete=models.CASCADE
    )
    quantity = models.CharField(
        max_length=100, blank=True, null=True
    )
    price_per_item = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True,
        help_text="Selling Price for a Single Item"
    )
    total_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    buying_price_item = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True,
        help_text='Buying Price for a Single Item'
    )
    total_buying_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    dated_order = models.DateField(blank=True, null=True)
    stock_expiry = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.product.name


class ProductDetail(DatedModel):
    product = models.ForeignKey(
        Product, related_name='product_detail',on_delete=models.CASCADE
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
        Product, related_name='purchased_product',on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        'pis_sales.SalesHistory', related_name='purchased_invoice',
        blank=True, null=True,on_delete=models.CASCADE
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
        'pis_retailer.Retailer', related_name='retailer_extra_items',on_delete=models.CASCADE
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
    product = models.ForeignKey(Product, related_name='claimed_product',on_delete=models.CASCADE)
    customer = models.ForeignKey(
        'pis_com.Customer', related_name='customer_claimed_items',
        null=True, blank=True,on_delete=models.CASCADE
    )
    claimed_items = models.IntegerField(
        default=1, verbose_name='No. of Claimed Items')
    claimed_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)

    def __unicode__(self):
        return self.product.name


class StockOut(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockout_product',on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        'pis_sales.SalesHistory', related_name='out_invoice',
        blank=True, null=True,on_delete=models.CASCADE
    )
    purchased_item = models.ForeignKey(
        PurchasedProduct, related_name='out_purchased',
        blank=True, null=True,on_delete=models.CASCADE
    )
    stock_out_quantity=models.CharField(max_length=100, blank=True, null=True)
    selling_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    buying_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    dated=models.DateField(blank=True, null=True)

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
