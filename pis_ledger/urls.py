from django.urls import re_path

from pis_ledger.views import (
    CustomerLedgerView, AddNewLedger, AddLedger,
    CustomerLedgerDetailsView,AddPayment
)

urlpatterns = [
    re_path(r'^add/new/$', AddNewLedger.as_view(), name='add_new_ledger'),
    re_path(r'^list/customer/$', CustomerLedgerView.as_view(),name='customer_ledger_list'),
    re_path(r'^add/customer/(?P<customer_id>\d+)/ledger/$',AddLedger.as_view(),name='add_ledger'),
    re_path(r'^add/customer/(?P<customer_id>\d+)/payment/$',AddPayment.as_view(),name='add_payment'),
    re_path(r'^customer/(?P<customer_id>\d+)/ledger/details/$',CustomerLedgerDetailsView.as_view(),name='customer_ledger_detail'),
]
