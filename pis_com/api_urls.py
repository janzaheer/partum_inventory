from django.urls import re_path


from pis_com.api_views import DailySalesAPI, WeeklySalesAPI, MonthlySalesAPI

urlpatterns = [
    re_path(r'^sales/daily/$', DailySalesAPI.as_view(),name='daily_sales_api'),
    re_path(r'^sales/weekly/$', WeeklySalesAPI.as_view(),name='weekly_sales_api'),
    re_path(r'^sales/monthly/$', MonthlySalesAPI.as_view(),name='monthly_sales_api'),
]
