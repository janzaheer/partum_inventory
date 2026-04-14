# -*- coding: utf-8 -*-
from django.contrib import admin
from pis_expense.models import ExtraExpense

class ExtraExpenseAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'amount', 'description', 'date'
    )
    search_fields = (
        'amount', 'description',
    )

    @staticmethod
    def amount(obj):
        return obj.amount

admin.site.register(ExtraExpense, ExtraExpenseAdmin)