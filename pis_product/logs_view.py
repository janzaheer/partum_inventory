from django.db.models import Sum, Count, Max
from django.views.generic import ListView

from django.utils import timezone

from pis_com.mixins import AuthRequiredMixin
from pis_product.models import StockOut


class DailyStockLogs(AuthRequiredMixin, ListView):
    model = StockOut
    template_name = 'logs/daily_stock_logs.html'
    paginate_by = 200

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target_date = None

    def _resolve_target_date(self):
        if self._target_date is not None:
            return self._target_date

        date_param = self.request.GET.get('date', '')
        if date_param:
            self._target_date = date_param
            return self._target_date

        retailer = self.request.user.retailer_user.retailer
        today = timezone.now().date()
        has_today = StockOut.objects.filter(
            product__retailer=retailer, dated=today
        ).exists()
        if has_today:
            self._target_date = today.strftime('%Y-%m-%d')
            return self._target_date

        latest = StockOut.objects.filter(
            product__retailer=retailer
        ).aggregate(latest=Max('dated'))['latest']
        if latest:
            self._target_date = latest.strftime('%Y-%m-%d')
        else:
            self._target_date = today.strftime('%Y-%m-%d')

        return self._target_date

    def _get_base_queryset(self):
        date_str = self._resolve_target_date()
        parts = date_str.split('-')
        year, month, day = parts[0], parts[1], parts[2]
        retailer = self.request.user.retailer_user.retailer
        return StockOut.objects.filter(
            product__retailer=retailer,
            dated__year=year, dated__month=month, dated__day=day,
        )

    def get_queryset(self):
        return self._get_base_queryset().values('product__name').annotate(
            receipt_item=Count('product__name'),
            total_qty=Sum('stock_out_quantity'),
        ).order_by('product__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = self._get_base_queryset()
        total = base_qs.aggregate(total=Sum('selling_price'))['total'] or 0

        date_str = self._resolve_target_date()
        date_param = self.request.GET.get('date', '')
        context.update({
            'total': total,
            'today_date': date_str if not date_param else None,
            'logs_date': date_param or date_str,
        })
        return context


class MonthlyStockLogs(AuthRequiredMixin, ListView):
    model = StockOut
    template_name = 'logs/monthly_stock_logs.html'
    paginate_by = 200

    MONTHS = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._month_label = ''
        self._year = ''
        self._base_qs = None

    def _get_base_queryset(self):
        if self._base_qs is not None:
            return self._base_qs

        retailer = self.request.user.retailer_user.retailer
        logs_month = self.request.GET.get('month')
        current_date = timezone.now().date()

        if logs_month:
            self._year = current_date.year
            month_index = self.MONTHS.index(logs_month) + 1
            if month_index > current_date.month:
                self._year -= 1
            self._month_label = logs_month
            self._base_qs = StockOut.objects.filter(
                product__retailer=retailer,
                dated__year=self._year, dated__month=month_index,
            )
        else:
            self._month_label = self.MONTHS[current_date.month - 1]
            self._year = current_date.year
            self._base_qs = StockOut.objects.filter(
                product__retailer=retailer,
                dated__year=current_date.year,
                dated__month=current_date.month,
            )

        return self._base_qs

    def get_queryset(self):
        return self._get_base_queryset().values('product__name').annotate(
            receipt_item=Count('product__name'),
            total_qty=Sum('stock_out_quantity'),
        ).order_by('product__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = self._get_base_queryset()
        total = base_qs.aggregate(total=Sum('selling_price'))['total'] or 0

        context.update({
            'total': total,
            'month': self._month_label,
            'year': self._year,
        })
        return context
