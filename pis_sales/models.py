# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from pis_com.models import DatedModel


class SalesHistory(DatedModel):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer', related_name='retailer_sales'
    )
    receipt_no = models.CharField(max_length=20)
    customer_name = models.CharField(
        max_length=100, blank=True, null=True
    )
    customer_phone = models.CharField(
        max_length=20, null=True, blank=True
    )
    product_details = models.TextField(
        max_length=512, blank=True, null=True,
        help_text='Quantity and Product name would save in JSON format')
    retail_amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    consumer_amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    total = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    discount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    profit = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )


