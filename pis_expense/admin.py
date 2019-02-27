# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from pis_expense.models import ExtraExpense

class ExtraExpenseAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'amount', 'description', 'date'
    )
    search_fields = (
        'amount', 'description',
    )

    @staticmethod
    def amount(obj):
        return obj.amount

admin.site.register(ExtraExpense, ExtraExpenseAdmin)