# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from pis_com.models import Customer
from pis_com.forms import CustomerForm
from pis_ledger.forms import LedgerForm


class AddNewLedger(FormView):
    form_class = CustomerForm
    template_name = 'ledger/create_ledger.html'

    def form_valid(self, form):
        customer = form.save()
        ledger_form_kwargs = {
            'retailer': self.request.POST.get('retailer'),
            'customer': customer.id,
            'amount': self.request.POST.get('amount'),
            'description': self.request.POST.get('description'),
        }

        ledger_form = LedgerForm(ledger_form_kwargs)
        if ledger_form.is_valid():
            ledger_form.save()

        return HttpResponseRedirect(reverse('ledger:customer_ledger_list'))

    def form_invalid(self, form):
        return super(AddNewLedger, self).form_invalid(form)


class AddLedger(FormView):
    template_name = 'ledger/add_customer_ledger.html'
    form_class = LedgerForm

    def form_valid(self, form):
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

    def get_context_data(self, **kwargs):
        context = super(CustomerLedgerView, self).get_context_data(**kwargs)
        customers = Customer.objects.filter(
            retailer=self.request.user.retailer_user.retailer
        )
        customer_ledger = []

        for customer in customers:
            customer_data = {}
            ledger = customer.customer_ledger.all().aggregate(Sum('amount'))
            payment_ledger = (
                customer.customer_ledger_payment.all()
                .aggregate(Sum('amount'))
            )

            if not ledger.get('amount__sum'):
                continue

            if payment_ledger.get('amount__sum'):
                payment_amount = float(payment_ledger.get('amount__sum'))
            else:
                payment_amount = 0

            remaining_ledger = '%g' % (
                    float(ledger.get('amount__sum')) -
                    payment_amount
            )

            customer_data.update({
                'id': customer.id,
                'ledger_amount': ledger.get('amount__sum'),
                'payment_amount': payment_amount,
                'customer_name': customer.customer_name,
                'customer_phone': customer.customer_phone,
                'remaining_ledger': remaining_ledger,
            })

            customer_ledger.append(customer_data)

        context.update({
            'customer_ledgers': customer_ledger
        })

        return context


class CustomerLedgerDetailsView(TemplateView):
    template_name = 'ledger/customer_ledger_details.html'

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
        payments = customer.customer_ledger_payment.all()
        if ledgers:
            ledger_total = ledgers.aggregate(Sum('amount'))
            ledger_total = float(ledger_total.get('amount__sum'))
            context.update({

            })
        else:
            ledger_total = 0

        if payments:
            payment_total = payments.aggregate(Sum('amount'))
            payment_total = float(payment_total.get('amount__sum'))
            context.update({

            })
        else:
            payment_total = 0

        context.update({
            'customer': customer,
            'ledgers': ledgers,
            'payments': payments,
            'ledger_total': '%g' % ledger_total,
            'payment_total': '%g' % payment_total,
            'remaining_amount': '%g' % (ledger_total - payment_total)
        })

        return context

