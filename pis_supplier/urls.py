from django.urls import re_path
from pis_supplier.views import(
    AddSupplier, SupplierList, SupplierStatementList, AddSupplierStatement,
    SupplierStatementUpdate,StatementPayment)


urlpatterns = [
    re_path(r'^add/$', AddSupplier.as_view(), name= 'add_supplier'),
    re_path(r'^lists/$', SupplierList.as_view(), name= 'list_supplier'),
    re_path(r'^statements/list/(?P<pk>\d+)/$',SupplierStatementList.as_view(),name='list_supplier_statement'),
    re_path(r'^statement/payment/(?P<pk>\d+)/$',StatementPayment.as_view(),name='payment'),
    re_path(r'^add/statements/(?P<pk>\d+)/$',AddSupplierStatement.as_view(),name='add_supplier_statement'),
    re_path(r'^update/statements/(?P<pk>\d+)/$',SupplierStatementUpdate.as_view(),name='update_supplier_statement')
]