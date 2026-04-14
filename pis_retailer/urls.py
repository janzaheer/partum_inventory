from django.urls import re_path

from pis_retailer.views import RetailerProductsAPI


urlpatterns = [
    re_path(r'^(?P<retailer_id>\d+)/products/$',RetailerProductsAPI.as_view(),name='retailer_products'),
]
