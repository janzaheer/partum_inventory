# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ast
import json

from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View, TemplateView
from django.utils import timezone

from pis_product.models import Product
from pis_sales.models import SalesHistory
from pis_product.forms import PurchasedProductForm
from pis_sales.forms import BillingForm
from pis_product.forms import ExtraItemForm
from pis_com.forms import CustomerForm
from pis_ledger.models import Ledger
from pis_ledger.forms import LedgerForm


class CreateInvoiceView(FormView):
    template_name = 'sales/create_invoice.html'
    form_class = BillingForm

    def get_context_data(self, **kwargs):
        context = super(CreateInvoiceView, self).get_context_data(**kwargs)
        products = (
            self.request.user.retailer_user.retailer.
                retailer_product.all()
        )
        customers = (
            self.request.user.retailer_user.
            retailer.retailer_customer.all()
        )
        context.update({
            'products': products,
            'customers': customers,
            'present_date': timezone.now().date(),
        })
        return context


class ProductItemAPIView(View):
    def get(self, request, *args, **kwargs):

        products = (
            self.request.user.retailer_user.retailer.
            retailer_product.all()
        )

        items = []

        for product in products:
            p = {
                'id': product.id,
                'name': product.name,
                'brand_name': product.brand_name,
            }

            if product.product_detail.exists():
                detail = product.product_detail.all().latest('id')
                p.update({
                    'retail_price': detail.retail_price,
                    'consumer_price': detail.consumer_price,
                })

                item = product.product_detail.aggregate(
                    available=Sum('available_item'),
                    purchased=Sum('purchased_item')
                )
                p.update({
                    'available_item': item.get('available'),
                    'purchased_item': item.get('purchased'),
                })

            items.append(p)

        return JsonResponse({'products': items})


class GenerateInvoiceAPIView(View):

    def __init__(self, *args, **kwargs):
        super(GenerateInvoiceAPIView, self).__init__(*args, **kwargs)
        self.customer = None
        self.invoice = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(
            GenerateInvoiceAPIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        customer_name = self.request.POST.get('customer_name')
        customer_phone = self.request.POST.get('customer_phone')
        sub_total = self.request.POST.get('sub_total')
        discount = self.request.POST.get('discount')
        shipping = self.request.POST.get('shipping')
        grand_total = self.request.POST.get('grand_total')
        totalQty = self.request.POST.get('totalQty')
        remaining_payment = self.request.POST.get('remaining_amount')
        paid_amount = self.request.POST.get('paid_amount')
        items = json.loads(self.request.POST.get('items'))
        purchased_items_id = []
        extra_items_id = []

        for item in items:
            item_name = item.get('item_name')
            try:
                product = Product.objects.get(
                    name=item_name,
                    retailer=self.request.user.retailer_user.retailer
                )
                form_kwargs = {
                    'product': product.id,
                    'quantity': item.get('qty'),
                    'price': item.get('price'),
                    'discount_percentage': item.get('perdiscount'),
                    'purchase_amount': item.get('total'),
                }
                form = PurchasedProductForm(form_kwargs)
                if form.is_valid():
                    purchased_item = form.save()
                    purchased_items_id.append(purchased_item.id)

                    product_details = (
                        purchased_item.product.product_detail.filter(
                            available_item__gte=int(item.get('qty'))).first()
                    )
                    product_details.available_item = (
                        product_details.available_item - int(
                            item.get('qty'))
                    )
                    product_details.purchased_item = (
                        product_details.purchased_item + int(
                            item.get('qty')))
                    product_details.save()

            except Product.DoesNotExist:
                extra_item_kwargs = {
                    'retailer': self.request.user.retailer_user.retailer.id,
                    'item_name': item.get('item_name'),
                    'quantity': item.get('qty'),
                    'price': item.get('price'),
                    'discount_percentage': item.get('perdiscount'),
                    'total': item.get('total'),
                }
                extra_item_form = ExtraItemForm(extra_item_kwargs)
                if extra_item_form.is_valid():
                    extra_item = extra_item_form.save()
                    extra_items_id.append(extra_item.id)

        billing_form_kwargs = {
            'sub_total': sub_total,
            'discount': discount,
            'grand_total': grand_total,
            'total_quantity': totalQty,
            'shipping': shipping,
            'purchased_items': purchased_items_id,
            'extra_items': extra_items_id,
            'paid_amount': paid_amount,
            'remaining_payment': remaining_payment,
            'retailer': self.request.user.retailer_user.retailer.id,
        }

        if self.request.POST.get('customer_id'):
            billing_form_kwargs.update({
                'customer': self.request.POST.get('customer_id')
            })
        else:
            customer_form_kwargs = {
                'customer_name': customer_name,
                'customer_phone': customer_phone,
                'retailer': self.request.user.retailer_user.retailer.id
            }
            customer_form = CustomerForm(customer_form_kwargs)
            if customer_form.is_valid():
                self.customer = customer_form.save()
                billing_form_kwargs.update({
                    'customer': self.customer.id
                })

        billing_form = BillingForm(billing_form_kwargs)
        if billing_form.is_valid():
            self.invoice = billing_form.save()

        if float(remaining_payment):
            ledger_form_kwargs = {
                'retailer': self.request.user.retailer_user.retailer.id,
                'customer': (
                    self.request.POST.get('customer_id') or
                    self.customer.id),
                'amount': remaining_payment,
                'description': (
                    'Remaining Payment for Bill/Receipt No %s '
                    % self.invoice.receipt_no)
            }

            ledger = LedgerForm(ledger_form_kwargs)
            if ledger.is_valid():
                ledger.save()

        return JsonResponse({'invoice_id': self.invoice.id})


class InvoiceDetailView(TemplateView):
    template_name = 'sales/invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        invoice = SalesHistory.objects.get(id=self.kwargs.get('invoice_id'))
        context.update({
            'invoice': invoice,
            'product_details': invoice.product_details,
            'extra_items_details': invoice.extra_items
        })
        return context


class InvoicesList(TemplateView):
    template_name = 'sales/invoice_list.html'

    @staticmethod
    def get_sales_history():
        return SalesHistory.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(InvoicesList, self).get_context_data(**kwargs)
        context.update({
            'invoices': self.get_sales_history(),
        })
        return context