from django.conf.urls import url, include

from pis_sales.views import (
    CreateBillingView, ProductItemAPIView, CreateInvoiceView,
    InvoiceDetailView
)

urlpatterns = [
    url(r'^bill/create/$', CreateBillingView.as_view(), name='bill_create'),
    url(
        r'^product/items/details/$',
        ProductItemAPIView.as_view(),
        name='product_item_api'
    ),
    url(
        r'^create/invoice/$',
        CreateInvoiceView.as_view(),
        name='create_invoice'
    ),
    # TODO: This url needs invoice ID to show the invoice detail
    url(r'^invoice/detail/$', InvoiceDetailView.as_view(), name='invoice_detail'),
]
