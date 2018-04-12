from django.conf.urls import url, include

from pis_sales.views import CreateBillingView, ProductItemAPIView

urlpatterns = [
    url(r'^bill/create/$', CreateBillingView.as_view(), name='bill_create'),
    url(
        r'^product/items/details/$',
        ProductItemAPIView.as_view(),
        name='product_item_api'
    ),
]
