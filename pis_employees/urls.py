from django.conf.urls import url

from pis_employees.views import (
    AddNewEmployee, EmployeeListView,EmployeeDelete
)

urlpatterns = [
    url(
        r'^add/new/$', AddNewEmployee.as_view(), name='add_new_employee'
    ),
    url(
        r'^list/$', EmployeeListView.as_view(),
        name='employee_list'
    ),
    url(
        r'delete/(?P<pk>\d+)/$',
        EmployeeDelete.as_view(),
        name='delete_employee'
    ),

]
