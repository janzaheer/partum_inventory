from django.conf.urls import url

from pis_expense.views import (
    AddNewExpense,ExpenseListView
)

urlpatterns = [
    url(
        r'^add/new/$', AddNewExpense.as_view(), name='add_new_expense'
    ),
    url(
        r'^list/$', ExpenseListView.as_view(),
        name='expense_list'
    ),
]
