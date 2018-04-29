from django.conf.urls import url, include

from pis_sales.views import (
    CreateBillingView, ProductItemAPIView, CreateInvoiceView,
    InvoiceDetailView, InvoicesList
)

urlpatterns = [
    url(r'^create/invoice/$', CreateBillingView.as_view(), name='bill_create'),
    url(
        r'^product/items/details/$',
        ProductItemAPIView.as_view(),
        name='product_item_api'
    ),
    url(
        r'^invoice/list/$',
        InvoicesList.as_view(),
        name='invoice_list'
    ),
    url(
        r'^create/invoice/$',
        CreateInvoiceView.as_view(),
        name='create_invoice'
    ),
    url(
        r'^invoice/(?P<invoice_id>\d+)/detail/$',
        InvoiceDetailView.as_view(),
        name='invoice_detail'
    ),
]
