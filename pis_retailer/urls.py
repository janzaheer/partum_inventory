from django.conf.urls import url, include

from pis_retailer.views import RetailerProductsAPI


urlpatterns = [
    url(
        r'^(?P<retailer_id>\d+)/products/$',
        RetailerProductsAPI.as_view(),
        name='retailer_products'
    ),
]
