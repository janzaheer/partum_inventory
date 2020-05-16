# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Sum

from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=250, null= True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    mobile_no = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def supplier_remaining_amount(self):
        supplier_statement = self.supplier.all()
        try:
            total_amount = supplier_statement.aggregate(Sum('supplier_amount'))
            total_amount = total_amount.get('supplier_amount__sum') or 0
            total_payments = supplier_statement.aggregate(Sum('payment_amount'))
            total_payments = total_payments.get('payment_amount__sum') or 0
        except:
            total_amount = 0
            total_payments = 0

        return total_amount - total_payments


class SupplierStatement(models.Model):
    supplier = models.ForeignKey(
        Supplier, related_name='supplier',
        null=True, blank=True,on_delete=models.CASCADE
                                 )
    supplier_amount = models.DecimalField(
        max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    payment_amount = models.DecimalField(
        max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    description = models.TextField(max_length=500, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.supplier.name if self.supplier else ''

    def remaining_amount(self):
        return self.supplier_amount - self.payment_amount
