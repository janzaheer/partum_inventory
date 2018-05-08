import json

from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Sum


class DailySalesAPI(View):

    @staticmethod
    def sales_data(obj, date):
        sales = obj.aggregate(
            total_sales=Sum('grand_total')
        )
        data = {
            'sales': sales.get('total_sales') or 0,
            'profit': 200,
            'date': date.strftime('%d-%b-%Y')
        }
        return data

    def get(self, request, *args, **kwargs):
        sales = []
        for day in range(7):
            sales_day = timezone.now() - relativedelta(days=day)
            retailer_sales = (
                self.request.user.retailer_user.retailer.
                retailer_sales.filter(created_at__icontains=sales_day.date())
            )
            data = self.sales_data(obj=retailer_sales, date=sales_day)
            sales.append(data)

        return JsonResponse(
            {'sales_data': sales}
        )
