# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from pis_com.models import Customer
from pis_com.forms import CustomerForm
from pis_ledger.forms import LedgerForm
from  pis_ledger.forms import Ledger


class AddNewLedger(FormView):
    form_class = CustomerForm
    template_name = 'ledger/create_ledger.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(AddNewLedger, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        customer = form.save()
        ledger_form_kwargs = {
            'retailer': self.request.POST.get('retailer'),
            'customer': customer.id,
            'person':self.request.POST.get('customer_type'),
            'amount': self.request.POST.get('amount'),
            'payment_amount': self.request.POST.get('payment_amount'),
            'payment_type': self.request.POST.get('payment_type'),
            'description': self.request.POST.get('description'),
        }

        ledger_form = LedgerForm(ledger_form_kwargs)
        if ledger_form.is_valid():
            ledger_form.save()

        return HttpResponseRedirect(reverse('ledger:customer_ledger_list'))

    def form_invalid(self, form):
        return super(AddNewLedger, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddNewLedger, self).get_context_data(**kwargs)
        customers = Customer.objects.filter(
            retailer=self.request.user.retailer_user.retailer)

        context.update({
            'customers': customers
        })

        return context


class AddLedger(FormView):
    template_name = 'ledger/add_customer_ledger.html'
    form_class = LedgerForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(AddLedger, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print(self.request.POST.get('dated'))
        print('+++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++')
        ledger = form.save()
        return HttpResponseRedirect(
            reverse('ledger:customer_ledger_detail', kwargs={
                'customer_id': self.kwargs.get('customer_id')
            })
        )

    def form_invalid(self, form):
        return super(AddLedger, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddLedger, self).get_context_data(**kwargs)
        try:
            customer = (
                self.request.user.retailer_user.retailer.
                retailer_customer.get(id=self.kwargs.get('customer_id'))
            )
        except ObjectDoesNotExist:
            raise Http404('Customer not found with concerned User')

        context.update({
            'customer': customer
        })
        return context


class CustomerLedgerView(TemplateView):
    template_name = 'ledger/customer_ledger_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            CustomerLedgerView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomerLedgerView, self).get_context_data(**kwargs)
        customers = (
            self.request.user.retailer_user.retailer.
            retailer_customer.all().order_by('customer_name')
        ).order_by('customer_name')
        customer_ledger = []

        for customer in customers:
            customer_data = {}
            ledger = customer.customer_ledger.all().aggregate(Sum('amount'))
            payment_ledger = (
                customer.customer_ledger.all()
                .aggregate(Sum('payment'))
            )

            if payment_ledger.get('payment__sum'):
                payment_amount = float(payment_ledger.get('payment__sum'))
            else:
                payment_amount = 0

            if ledger.get('amount__sum'):
                ledger_amount = float(ledger.get('amount__sum'))
            else:
                ledger_amount = 0

            remaining_ledger = '%g' % (
                    ledger_amount - payment_amount
            )
            customer_data.update({
                'id': customer.id,
                'ledger_amount': ledger_amount,
                'payment_amount': payment_amount,
                'customer_name': customer.customer_name,
                'customer_phone': customer.customer_phone,
                'remaining_ledger': remaining_ledger,
                'customer_type':customer.customer_type,
            })

            customer_ledger.append(customer_data)

        ledgers = Ledger.objects.all()
        if ledgers:
            grand_ledger = ledgers.aggregate(Sum('amount'))
            grand_ledger = float(grand_ledger.get('amount__sum') or 0)

            grand_payment = ledgers.aggregate(Sum('payment'))
            grand_payment = float(grand_payment.get('payment__sum') or 0)

            total_remaining_amount = grand_ledger - grand_payment
        else:
            total_remaining_amount = 0

        context.update({
            'customer_ledgers': customer_ledger,
            'total_remaining_amount': total_remaining_amount,
        })

        return context


class CustomerLedgerDetailsView(TemplateView):
    template_name = 'ledger/customer_ledger_details.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            CustomerLedgerDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            CustomerLedgerDetailsView, self).get_context_data(**kwargs)

        try:
            customer = Customer.objects.get(
                id=self.kwargs.get('customer_id')
            )
        except Customer.DoesNotExist:
            raise Http404

        ledgers = customer.customer_ledger.all()
        if ledgers:
            ledger_total = ledgers.aggregate(Sum('amount'))
            ledger_total = float(ledger_total.get('amount__sum'))
            context.update({

            })
        else:
            ledger_total = 0

        if ledgers:
            payment_total = ledgers.aggregate(Sum('payment'))
            payment_total = float(payment_total.get('payment__sum'))
            context.update({

            })
        else:
            payment_total = 0

        context.update({
            'customer': customer,
            'ledgers': ledgers.order_by('-dated'),
            'ledger_total': '%g' % ledger_total,
            'payment_total': '%g' % payment_total,
            'remaining_amount': '%g' % (ledger_total - payment_total)
        })

        return context


class AddPayment(FormView):
    template_name = 'ledger/add_payment.html'
    form_class = LedgerForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(AddPayment, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        ledger = form.save()
        return HttpResponseRedirect(
            reverse('ledger:customer_ledger_detail', kwargs={
                'customer_id': self.kwargs.get('customer_id')
            })
        )

    def form_invalid(self, form):
        return super(AddPayment, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddPayment, self).get_context_data(**kwargs)
        try:
            customer = (
                self.request.user.retailer_user.retailer.
                retailer_customer.get(id=self.kwargs.get('customer_id'))
            )
        except ObjectDoesNotExist:
            raise Http404('Customer not found with concerned User')

        context.update({
            'customer': customer
        })
        return context
