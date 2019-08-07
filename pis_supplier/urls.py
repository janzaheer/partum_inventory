from django.conf.urls import url
from pis_supplier.views import(
    AddSupplier, SupplierList, SupplierStatementList, AddSupplierStatement,
    SupplierStatementUpdate,StatementPayment)


urlpatterns = [
    url(
        r'^add/$', AddSupplier.as_view(), name= 'add_supplier'
    ),

    url(
        r'^lists/$', SupplierList.as_view(), name= 'list_supplier'
    ),

    url(
        r'^statements/list/(?P<pk>\d+)/$',
        SupplierStatementList.as_view(),
        name='list_supplier_statement'
    ),
    url(
        r'^statement/payment/(?P<pk>\d+)/$',
        StatementPayment.as_view(),
        name='payment'
    ),

    url(
        r'^add/statements/(?P<pk>\d+)/$',
        AddSupplierStatement.as_view(),
        name='add_supplier_statement'
    ),
    url(r'^update/statements/(?P<pk>\d+)/$',
        SupplierStatementUpdate.as_view(),
        name='update_supplier_statement'
    )
]