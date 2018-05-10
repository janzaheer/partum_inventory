from django.conf.urls import url

from pis_com.api_views import DailySalesAPI, WeeklySalesAPI

urlpatterns = [
    url(r'^sales/daily/$', DailySalesAPI.as_view(), name='daily_sales_api'),
    url(r'^sales/weekly/$', WeeklySalesAPI.as_view(), name='weekly_sales_api'),

]