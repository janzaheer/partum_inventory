# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.views.generic import FormView, DeleteView, ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from pis_com.models import Customer
from pis_employees.forms import EmployeeSalaryForm, EmployeeForm
from pis_employees.models import EmployeeSalary, Employee

class AddNewEmployee(FormView):
    form_class = EmployeeForm
    template_name = "employee/create.html"
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(AddNewEmployee, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
     form.save()
     return HttpResponseRedirect(reverse('employee:employee_list'))

    def form_invalid(self, form):
        return super(AddNewEmployee, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddNewEmployee, self).get_context_data(**kwargs)
        customers = Customer.objects.filter(
            retailer=self.request.user.retailer_user.retailer)

        context.update({
            'customers': customers
        })
        return context

class EmployeeListView(ListView):
    template_name = 'employee/employee_list.html'
    model = Employee
    paginate_by = 150
    is_paginated = True

    def get_queryset(self):
        query_set = Employee.objects.all().order_by('-date_of_joining')
        return query_set

class EmployeeDelete(DeleteView):
    model= Employee
    success_url= reverse_lazy('employee:employee_list')
    success_message=''

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

