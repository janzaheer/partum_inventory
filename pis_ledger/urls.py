from django.conf.urls import url

from pis_ledger.views import (
    CustomerLedgerView, AddNewLedger, AddLedger,
    CustomerLedgerDetailsView
)


urlpatterns = [
    url(
        r'^add/new/$', AddNewLedger.as_view(), name='add_new_ledger'
    ),
    url(
        r'^list/customer/$', CustomerLedgerView.as_view(),
        name='customer_ledger_list'
    ),
    url(
        r'^add/customer/(?P<customer_id>\d+)/ledger/$',
        AddLedger.as_view(),
        name='add_ledger'
    ),
    url(
        r'^customer/(?P<customer_id>\d+)/ledger/details/$',
        CustomerLedgerDetailsView.as_view(),
        name='customer_ledger_detail'
    )
]
