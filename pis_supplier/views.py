# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.views.generic import FormView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from pis_supplier.models import Supplier, SupplierStatement
from pis_supplier.forms import SupplierForm, SupplierStatementForm
from django.db.models import Sum


class AddSupplier(FormView):
    form_class = SupplierForm
    template_name = 'supplier/add_supplier.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            AddSupplier, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        return HttpResponseRedirect(reverse('supplier:list_supplier'))

    def form_invalid(self, form):
        return super(AddSupplier, self).form_invalid(form)


class SupplierList(ListView):
    template_name = 'supplier/list_supplier.html'
    model = Supplier
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            SupplierList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SupplierList, self).get_context_data(**kwargs)
        supplier_statements = SupplierStatement.objects.all()
        try:
            supplier_amounts = supplier_statements.aggregate(Sum('supplier_amount'))
            supplier_amounts = supplier_amounts.get('supplier_amount__sum') or 0
            payment_amounts = supplier_statements.aggregate(Sum('payment_amount'))
            payment_amounts = payment_amounts.get('payment_amount__sum') or 0
        except:
            supplier_amounts = 0
            payment_amounts = 0

        total_remaining_amount = supplier_amounts - payment_amounts
        context.update({
            'total_remaining_amount':total_remaining_amount
        })
        return context


class SupplierStatementList(ListView):
    template_name = 'supplier/list_supplier_statement.html'
    model = SupplierStatement
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            SupplierStatementList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query_set = SupplierStatement.objects.filter(
            supplier__id=self.kwargs.get('pk')).order_by('-date')
        if self.request.GET.get('date'):
            query_set= query_set.filter(
                supplier__name__contains=self.request.GET.get('date')
            )
        return query_set

    def get_context_data(self, **kwargs):
        context = super(SupplierStatementList, self).get_context_data(**kwargs)
        supplier_statements = SupplierStatement.objects.filter(supplier__id=self.kwargs.get('pk'))
        supplier = (
            Supplier.objects.get(id=self.kwargs.get('pk'))
        )
        try:
            supplier_amounts = supplier_statements.aggregate(Sum('supplier_amount'))
            supplier_amounts = supplier_amounts.get('supplier_amount__sum') or 0
            payment_amounts = supplier_statements.aggregate(Sum('payment_amount'))
            payment_amounts = payment_amounts.get('payment_amount__sum') or 0
        except:
            supplier_amounts = 0
            payment_amounts = 0

        supplier_total_remaining_amount = supplier_amounts - payment_amounts

        context.update({
            'supplier': supplier,
            'supplier_total_remaining_amount':supplier_total_remaining_amount
        })
        return context


class AddSupplierStatement(FormView):
    form_class = SupplierStatementForm
    template_name = 'supplier/add_supplier_statement.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            AddSupplierStatement, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        obj.supplier = Supplier.objects.get(name=self.request.POST.get('supplier_name'))
        obj.save()
        return HttpResponseRedirect(reverse(
            'supplier:list_supplier_statement',kwargs={
                'pk':obj.supplier.id}))

    def form_invalid(self, form):
        print(form.errors)
        return super(AddSupplierStatement, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddSupplierStatement, self).get_context_data(**kwargs)
        supplier = (
            Supplier.objects.get(id=self.kwargs.get('pk'))
        )
        context.update({
            'supplier': supplier
        })
        return context


class SupplierStatementUpdate(UpdateView):
    template_name = 'supplier/update_supplier_statement.html'
    model = SupplierStatement
    form_class = SupplierStatementForm

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse('supplier:list_supplier_statement', kwargs={'pk':obj.supplier.id})
        )

    def form_invalid(self, form):
        return super(SupplierStatementUpdate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(SupplierStatementUpdate, self).get_context_data(**kwargs)
        supplier = (
            Supplier.objects.get(supplier__id=self.kwargs.get('pk'))
        )
        context.update({
            'supplier': supplier
        })
        return context


class StatementPayment(FormView):
    form_class = SupplierStatementForm
    template_name = 'supplier/payment.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            StatementPayment, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(reverse(
            'supplier:list_supplier_statement', kwargs={
                'pk': self.kwargs.get('pk')}))

    def form_invalid(self, form):
        return super(StatementPayment, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StatementPayment, self).get_context_data(**kwargs)
        supplier = (
            Supplier.objects.get(id=self.kwargs.get('pk'))
        )
        context.update({
            'supplier': supplier
        })
        return context