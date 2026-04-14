from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from datetime import timedelta

from pis_com.mixins import AuthRequiredMixin
from pis_sales.models import SalesHistory
from pis_product.models import StockOut


class DailySalesAPI(AuthRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        retailer = request.user.retailer_user.retailer
        today = timezone.now().date()
        start_date = today - timedelta(days=6)

        sales_by_day = dict(
            SalesHistory.objects.filter(
                retailer=retailer,
                created_at__date__gte=start_date,
                created_at__date__lte=today,
            ).annotate(
                day=TruncDate('created_at')
            ).values('day').annotate(
                total=Sum('grand_total')
            ).values_list('day', 'total')
        )

        profit_by_day = dict(
            StockOut.objects.filter(
                product__retailer=retailer,
                dated__gte=start_date,
                dated__lte=today,
            ).values('dated').annotate(
                selling=Sum('selling_price'),
                buying=Sum('buying_price'),
            ).values_list('dated', 'selling')
        )

        buying_by_day = dict(
            StockOut.objects.filter(
                product__retailer=retailer,
                dated__gte=start_date,
                dated__lte=today,
            ).values('dated').annotate(
                buying=Sum('buying_price'),
            ).values_list('dated', 'buying')
        )

        sales_data = []
        for i in range(7):
            day = today - timedelta(days=i)
            total_sales = sales_by_day.get(day) or Decimal('0')
            selling = profit_by_day.get(day) or Decimal('0')
            buying = buying_by_day.get(day) or Decimal('0')
            sales_data.append({
                'date': day.strftime('%Y-%m-%d'),
                'sales': float(total_sales),
                'profit': float(selling - buying),
            })

        return JsonResponse({'sales_data': sales_data})


class WeeklySalesAPI(AuthRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        retailer = request.user.retailer_user.retailer
        today = timezone.now().date()
        sales_data = []

        for i in range(4):
            week_end = today - timedelta(weeks=i)
            week_start = week_end - timedelta(days=6)

            total_sales = SalesHistory.objects.filter(
                retailer=retailer,
                created_at__date__gte=week_start,
                created_at__date__lte=week_end,
            ).aggregate(total=Sum('grand_total'))['total'] or Decimal('0')

            stock_agg = StockOut.objects.filter(
                product__retailer=retailer,
                dated__gte=week_start,
                dated__lte=week_end,
            ).aggregate(
                selling=Sum('selling_price'),
                buying=Sum('buying_price'),
            )
            profit = (stock_agg['selling'] or Decimal('0')) - (stock_agg['buying'] or Decimal('0'))

            sales_data.append({
                'date': f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}",
                'sales': float(total_sales),
                'profit': float(profit),
            })

        return JsonResponse({'sales_data': sales_data})


class MonthlySalesAPI(AuthRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        retailer = request.user.retailer_user.retailer
        today = timezone.now().date()
        month_start = today.replace(day=1)

        sales_by_day = dict(
            SalesHistory.objects.filter(
                retailer=retailer,
                created_at__date__gte=month_start,
                created_at__date__lte=today,
            ).annotate(
                day=TruncDate('created_at')
            ).values('day').annotate(
                total=Sum('grand_total')
            ).values_list('day', 'total')
        )

        stock_by_day = (
            StockOut.objects.filter(
                product__retailer=retailer,
                dated__gte=month_start,
                dated__lte=today,
            ).values('dated').annotate(
                selling=Sum('selling_price'),
                buying=Sum('buying_price'),
            )
        )
        selling_by_day = {row['dated']: row['selling'] or Decimal('0') for row in stock_by_day}
        buying_by_day = {row['dated']: row['buying'] or Decimal('0') for row in stock_by_day}

        sales_data = []
        current = month_start
        while current <= today:
            total_sales = sales_by_day.get(current) or Decimal('0')
            selling = selling_by_day.get(current, Decimal('0'))
            buying = buying_by_day.get(current, Decimal('0'))

            sales_data.append({
                'day': current.strftime('%b %d'),
                'sales': float(total_sales),
                'profit': float(selling - buying),
            })
            current += timedelta(days=1)

        return JsonResponse({'sales_data': sales_data})
