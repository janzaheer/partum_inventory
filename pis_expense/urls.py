from django.urls import re_path


from pis_expense.views import (
    AddNewExpense,ExpenseListView,ExpenseDelete,dashboard
)

urlpatterns = [
    re_path(r'^add/new/$', AddNewExpense.as_view(), name='add_new_expense'),
    re_path(r'^list/$', ExpenseListView.as_view(),name='expense_list'),
    re_path(r'^dashboard/$', dashboard.as_view(),name='dashboard'),
    re_path(r'delete/(?P<pk>\d+)/$',ExpenseDelete.as_view(),name='delete_expense'),
]
