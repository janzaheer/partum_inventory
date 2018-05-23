# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from pis_com.models import DatedModel


class Ledger(DatedModel):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer', related_name='retailer_ledger', blank=True, null=True)
    customer = models.ForeignKey(
        'pis_com.Customer', related_name='customer_ledger'
    )
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.customer.customer_name


class PaymentLedger(DatedModel):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer', related_name='retailer_ledger_payment', blank=True, null=True)
    customer = models.ForeignKey(
        'pis_com.Customer', related_name='customer_ledger_payment'
    )
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, blank=True, null=True
    )

    def __unicode__(self):
        return self.customer.customer_name
