from django.urls import re_path

from pis_employees.views import (
    AddNewEmployee, EmployeeListView,EmployeeDelete,EmployeeSalaryView,
    EmployeeSalaryDetail
)

urlpatterns = [
    re_path(r'^add/new/$', AddNewEmployee.as_view(), name='add_new_employee'),
    re_path(r'^list/$', EmployeeListView.as_view(),name='employee_list'),
    re_path(r'delete/(?P<pk>\d+)/$',EmployeeDelete.as_view(),name='delete_employee'),
    re_path(r'salary/(?P<pk>\d+)/$',EmployeeSalaryView.as_view(),name='employee_salary'),
    re_path(r'salary/(?P<pk>\d+)/detail/$',EmployeeSalaryDetail.as_view(),name='employee_salary_detail'),
]
