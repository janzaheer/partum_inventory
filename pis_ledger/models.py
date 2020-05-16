# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from pis_com.models import DatedModel


class Ledger(DatedModel):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer', related_name='retailer_ledger', blank=True, null=True,on_delete=models.CASCADE)
    customer = models.ForeignKey(
        'pis_com.Customer', related_name='customer_ledger',on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        'pis_sales.SalesHistory', related_name='ledger_invoice',
        blank=True, null=True,on_delete=models.CASCADE
    )
    person=models.CharField(max_length=200, default='customer', blank=True, null=True)
    amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    payment_type = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    dated = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.customer.customer_name

