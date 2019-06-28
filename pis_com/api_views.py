import json
import datetime

from calendar import monthrange
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Sum

from pis_product.models import StockOut


class DailySalesAPI(View):

    @staticmethod
    def sales_data(obj, stockout=None, date=None, week_date=None, month_date=None):
        sales = obj.aggregate(
            total_sales=Sum('grand_total')
        )

        data = {
            'sales': (
                int(sales.get('total_sales')) if
                sales.get('total_sales') else 0
            ),
        }

        profit = 0
        if stockout:
            try:
                selling_amount = stockout.aggregate(selling_amount=Sum('selling_price'))
                buying_amount = stockout.aggregate(buying_amount=Sum('buying_price'))
                selling_amount = selling_amount.get('selling_amount') or 0
                buying_amount = buying_amount.get('buying_amount') or 0
            except:
                selling_amount = 0
                buying_amount = 0

            profit = float(selling_amount) - float(buying_amount)
        data.update({
            'profit': profit
        })

        if week_date:
            data.update({
                'date': week_date.strftime('%a %d, %b')
            })
        elif month_date:
            data.update({
                'day': month_date.strftime('%b')
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

            retailer_products = (self.request.user.retailer_user.retailer.
                    retailer_product.all().values_list('id', flat=True))

            stockout = StockOut.objects.filter(
                dated__icontains=sales_day.date(),
                product__in=retailer_products
            )

            data = self.sales_data(
                obj=retailer_sales, stockout=stockout, date=sales_day
            )
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
            retailer_products = (self.request.user.retailer_user.retailer.
                                 retailer_product.all().values_list('id',
                                                                    flat=True))

            stockout = StockOut.objects.filter(
                dated__gte=sales_start_week,
                dated__lt=sales_end_week,
                product__in=retailer_products
            )
            data = self.sales_data(
                obj=retailer_sales, stockout=stockout, week_date=sales_end_week
            )
            sales.append(data)

        return JsonResponse(
            {'sales_data': sales}
        )


class MonthlySalesAPI(DailySalesAPI):
    def get(self, request, *args, **kwargs):
        sales = []

        for month in range(12):
            date_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(
                date_month.year, date_month.month
            )
            start_month = datetime.datetime(
                date_month.year, date_month.month, 1)

            end_month = datetime.datetime(
                date_month.year, date_month.month, month_range[1]
            )

            retailer_sales = (
                self.request.user.retailer_user.retailer.retailer_sales.filter(
                    created_at__gte=start_month,
                    created_at__lt=end_month.replace(
                        hour=23, minute=59, second=59)
                )
            )

            retailer_products = (self.request.user.retailer_user.retailer.
                                 retailer_product.all().values_list('id',
                                                                    flat=True))
            stockout = StockOut.objects.filter(
                dated__gte=start_month,
                dated__lt=end_month.replace(
                        hour=23, minute=59, second=59),
                product__in=retailer_products
            )

            data = self.sales_data(
                obj=retailer_sales, stockout=stockout, month_date=end_month
            )
            sales.append(data)

        return JsonResponse(
            {'sales_data': sales}
        )
