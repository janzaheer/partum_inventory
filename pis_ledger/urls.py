from django.conf.urls import url

from pis_ledger.views import CustomerLedgerView , AddNewLedger, AddLedger


urlpatterns = [
    url(
        r'^add/new/$', AddNewLedger.as_view(), name='add_new_ledger'
    ),
    url(
        r'^list/customer/$', CustomerLedgerView.as_view(),
        name='customer_ledger_list'
    ),
    url(
        r'^add/(?P<customer_id>\d+)/ledger/$',
        AddLedger.as_view(),
        name='add_ledger'
    ),
]
