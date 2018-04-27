# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.db import models
from django.db.models.signals import post_save

from pis_com.models import DatedModel


class SalesHistory(DatedModel):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer', related_name='retailer_sales'
    )
    receipt_no = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )

    customer = models.ForeignKey(
        'pis_sales.Customer',
        related_name='customer_sales',
        blank=True, null=True
    )

    product_details = models.TextField(
        max_length=512, blank=True, null=True,
        help_text='Quantity and Product name would save in JSON format')

    purchased_items = models.ManyToManyField(
        'pis_product.PurchasedProduct',
        max_length=100, blank=True, null=True
    )

    total_quantity = models.CharField(
        max_length=10, blank=True, null=True, default=1)

    sub_total = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )

    remaining_payment = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )

    discount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )

    shipping = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )

    grand_total = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )

    def __unicode__(self):
        return self.retailer.name


class Customer(models.Model):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer',
        related_name='retailer_customer'
    )
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.customer_name


# Signals Function
def create_save_receipt_no(sender, instance, created, **kwargs):
    if created and not instance.receipt_no:
        while True:
            random_code = random.randint(1000000, 9999999)
            if (
                not SalesHistory.objects.filter(
                    receipt_no=random_code).exists()
            ):
                break

        instance.receipt_no = random_code
        instance.save()


# Signal Calls
post_save.connect(create_save_receipt_no, sender=SalesHistory)
