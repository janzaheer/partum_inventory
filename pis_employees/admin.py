# -*- coding: utf-8 -*-
from django.contrib import admin
from pis_employees.models import Employee, EmployeeSalary
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'name', 'father_name', 'mobile', 'address','date_of_joining'
    )
    search_fields = (
        'name', 'cnic',
    )

    @staticmethod
    def name(obj):
        return obj.name


class EmployeeSalaryAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'employee' ,'salary_amount', 'date'
    )

    @staticmethod
    def employee(obj):
        return obj.employee.name
    search_fields = (
         'date',
    )

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeSalary, EmployeeSalaryAdmin)