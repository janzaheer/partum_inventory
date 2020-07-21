from django.urls import re_path


from pis_sales.views import (
    GenerateInvoiceAPIView, ProductItemAPIView, CreateInvoiceView,
    UpdateInvoiceView, InvoiceDetailView, UpdateInvoiceAPIView, InvoicesList,
    ProductDetailsAPIView, SalesDeleteView
)

urlpatterns = [
    re_path(r'^create/invoice/$',CreateInvoiceView.as_view(),name='create_invoice'),
    re_path(r'^update/(?P<id>\d+)/api/$',UpdateInvoiceView.as_view(),name='invoice_update'),
    re_path(r'^product/items/details/$',ProductItemAPIView.as_view(),name='product_item_api'),
    re_path(r'^invoice/list/$',InvoicesList.as_view(),name='invoice_list'),
    re_path(r'^api/generate/invoice/$',GenerateInvoiceAPIView.as_view(),name='generate_invoice_api'),
    re_path(r'^api/update/invoice/$',UpdateInvoiceAPIView.as_view(),name='update_invoice_api'),
    re_path(r'^invoice/(?P<invoice_id>\d+)/detail/$',InvoiceDetailView.as_view(),name='invoice_detail'),
    re_path(r'^api/product/details/$',ProductDetailsAPIView.as_view(),name='product_details_api'),
    re_path(r'^invoice/(?P<pk>\d+)/delete/$',SalesDeleteView.as_view(),name='delete'),
]
