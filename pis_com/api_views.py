import json

from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Sum


class DailySalesAPI(View):

    @staticmethod
    def sales_data(obj, date=None, week_date=None, month_date=None):
        sales = obj.aggregate(
            total_sales=Sum('grand_total')
        )
        data = {
            'sales': (
                int(sales.get('total_sales')) if
                sales.get('total_sales') else 0
            ),
            'profit': 200,
        }
        if week_date:
            data.update({
                'date': week_date.strftime('%a %d, %b')
            })
        elif month_date:
            data.update({
                'date': month_date.strftime('%d, %B')
            })
        else:
            data.update({
                'date': date.strftime('%d-%b-%Y')
            })
        return data

    def get(self, request, *args, **kwargs):
        sales = []
        for day in range(12):
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


class WeeklySalesAPI(DailySalesAPI):

    def get(self, request, *args, **kwargs):
        sales = []
        for week in xrange(1, 13):
            sales_start_week = timezone.now() - relativedelta(weeks=week)
            sales_end_week = timezone.now() - relativedelta(weeks=week - 1)

            retailer_sales = (
                self.request.user.retailer_user.retailer.retailer_sales.filter(
                    created_at__gte=sales_start_week,
                    created_at__lt=sales_end_week
                )
            )
            data = self.sales_data(
                obj=retailer_sales, week_date=sales_end_week
            )
            sales.append(data)

        return JsonResponse(
            {'sales_data': sales}
        )


class MonthlySalesAPI(DailySalesAPI):
    def get(self, request, *args, **kwargs):
        sales = []
        for month in xrange(1, 13):
            sales_start_month = timezone.now() - relativedelta(months=month)
            sales_end_month = timezone.now() - relativedelta(months=month - 1)

            retailer_sales = (
                self.request.user.retailer_user.retailer.retailer_sales.filter(
                    created_at__gte=sales_start_month.replace(
                        day=1, minute=0, second=0, hour=0),
                    created_at__lt=sales_end_month.replace(
                        day=1, minute=0, second=0, hour=0)
                )
            )

            data = self.sales_data(
                obj=retailer_sales, month_date=sales_end_month
            )

            sales.append(data)

        return JsonResponse(
            {'sales_data': sales}
        )

