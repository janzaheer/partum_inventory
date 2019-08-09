from django.contrib import admin
from pis_ledger.models import Ledger


class LedgerAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'retailer','invoice','person', 'amount','payment',
        'description','dated', 'created_at'
    )
    search_fields = (
        'customer__customer_name', 'customer__customer_phone',
        'customer__person_type','customer__retailer__name'
    )
    raw_id_fields = ('customer',)

    @staticmethod
    def retailer(obj):
        return obj.retailer.name


admin.site.register(Ledger, LedgerAdmin)
