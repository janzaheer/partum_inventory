# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from pis_sales.models import SalesHistory


class SalesHistoryAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'customer_name', 'customer_phone',
        'receipt_no', 'created_at'
    )
    search_fields = (
        'retailer__name', 'customer__customer_name',
        'customer__customer_phone', 'receipt_no'
    )
    raw_id_fields = ('retailer', 'customer')

    @staticmethod
    def customer_name(obj):
        return obj.customer.customer_name if obj.customer else ''

    @staticmethod
    def customer_phone(obj):
        return obj.customer.customer_phone if obj.customer else ''

    @staticmethod
    def retailer(obj):
        return obj.retailer.name


admin.site.register(SalesHistory, SalesHistoryAdmin)
