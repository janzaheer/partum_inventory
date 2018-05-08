from django.conf.urls import url

from pis_com.api_views import DailySalesAPI

urlpatterns = [
    url(r'^sales/daily/$', DailySalesAPI.as_view(), name='index'),

]