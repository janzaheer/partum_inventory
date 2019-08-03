# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pis_supplier.models import Supplier, SupplierStatement

from django.contrib import admin

# Register your models here.
# class SupplierAdmin(admin.ModelAdmin):
#     list_display = ('name', 'address', 'phone', 'mobile_no',)


admin.site.register(Supplier)
admin.site.register(SupplierStatement)
