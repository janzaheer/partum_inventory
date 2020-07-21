# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.views.generic import FormView, DeleteView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render

from pis_com.models import Customer
from pis_expense.forms import ExtraExpenseForm
from pis_expense.models import ExtraExpense

class AddNewExpense(FormView):
    form_class = ExtraExpenseForm
    template_name = 'expense/create_expense.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(AddNewExpense, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
     form.save()
     return HttpResponseRedirect(reverse('expense:expense_list'))

    def form_invalid(self, form):
        return super(AddNewExpense, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddNewExpense, self).get_context_data(**kwargs)
        customers = Customer.objects.filter(
            retailer=self.request.user.retailer_user.retailer)

        context.update({
            'customers': customers
        })

        return context

class ExpenseListView(ListView):
    template_name = 'expense/expense_list.html'
    model = ExtraExpense
    paginate_by = 150
    is_paginated = True

    def get_queryset(self):
        query_set = ExtraExpense.objects.all().order_by('-date')
        return query_set

class ExpenseDelete(DeleteView):
    model= ExtraExpense
    success_url= reverse_lazy('expense:expense_list')
    success_message=''

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class dashboard(TemplateView):
    template_name = 'expense/dashboard.html'
