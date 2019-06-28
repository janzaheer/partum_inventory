from django.conf.urls import url

from pis_expense.views import (
    AddNewExpense,ExpenseListView,ExpenseDelete,dashboard
)

urlpatterns = [
    url(
        r'^add/new/$', AddNewExpense.as_view(), name='add_new_expense'
    ),
    url(
        r'^list/$', ExpenseListView.as_view(),
        name='expense_list'
    ),
url(
        r'^dashboard/$', dashboard.as_view(),
        name='dashboard'
    ),
    url(
        r'delete/(?P<pk>\d+)/$',
        ExpenseDelete.as_view(),
        name='delete_expense'
    ),
]
