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
        'retailer__name', 'customer_name', 'customer_phone', 'receipt_no'
    )
    raw_id_fields = ('retailer',)


admin.site.register(SalesHistory, SalesHistoryAdmin)
