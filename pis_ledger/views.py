from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.db.models import Sum
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from pis_com.mixins import AuthRequiredMixin
from pis_com.models import Customer
from pis_ledger.forms import LedgerForm
from pis_ledger.models import Ledger


class AddNewLedger(AuthRequiredMixin, FormView):
    form_class = LedgerForm
    template_name = 'ledger/create_ledger.html'

    def form_valid(self, form):
        ledger = form.save(commit=False)
        ledger.retailer = self.request.user.retailer_user.retailer
        ledger.save()
        return HttpResponseRedirect(reverse('ledger:customer_ledger_list'))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = Customer.objects.filter(
            retailer=self.request.user.retailer_user.retailer)
        context.update({
            'customers': customers
        })
        return context


class AddLedger(AuthRequiredMixin, FormView):
    template_name = 'ledger/add_customer_ledger.html'
    form_class = LedgerForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(
            reverse('ledger:customer_ledger_detail', kwargs={
                'customer_id': self.kwargs.get('customer_id')
            })
        )

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class CustomerLedgerView(AuthRequiredMixin, TemplateView):
    template_name = 'ledger/customer_ledger_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        retailer = self.request.user.retailer_user.retailer
        customers = retailer.retailer_customer.all().order_by('customer_name')
        customer_ledger = []

        for customer in customers:
            customer_data = {}
            ledger = customer.customer_ledger.all().aggregate(Sum('amount'))
            payment_ledger = (
                customer.customer_ledger.all().aggregate(Sum('payment'))
            )

            payment_amount = float(payment_ledger.get('payment__sum') or 0)
            ledger_amount = float(ledger.get('amount__sum') or 0)

            remaining_ledger = '%g' % (ledger_amount - payment_amount)
            customer_data.update({
                'id': customer.id,
                'ledger_amount': ledger_amount,
                'payment_amount': payment_amount,
                'customer_name': customer.customer_name,
                'customer_phone': customer.customer_phone,
                'remaining_ledger': remaining_ledger,
                'customer_type': customer.customer_type,
            })

            customer_ledger.append(customer_data)

        ledgers = Ledger.objects.filter(retailer=retailer)
        if ledgers.exists():
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


class CustomerLedgerDetailsView(AuthRequiredMixin, TemplateView):
    template_name = 'ledger/customer_ledger_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            customer = self.request.user.retailer_user.retailer.retailer_customer.get(
                id=self.kwargs.get('customer_id')
            )
        except Customer.DoesNotExist:
            raise Http404

        ledgers = customer.customer_ledger.all()
        if ledgers:
            ledger_total = ledgers.aggregate(Sum('amount'))
            ledger_total = float(ledger_total.get('amount__sum') or 0)
        else:
            ledger_total = 0

        if ledgers:
            payment_total = ledgers.aggregate(Sum('payment'))
            payment_total = float(payment_total.get('payment__sum') or 0)
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


class AddPayment(AuthRequiredMixin, FormView):
    template_name = 'ledger/add_payment.html'
    form_class = LedgerForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(
            reverse('ledger:customer_ledger_detail', kwargs={
                'customer_id': self.kwargs.get('customer_id')
            })
        )

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
