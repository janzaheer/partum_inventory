from django.urls import path, include

from pis_retailer.views import RetailerProductsAPI


urlpatterns = [
    path(
        r'^(?P<retailer_id>\d+)/products/$',
        RetailerProductsAPI.as_view(),
        name='retailer_products'
    ),
]
