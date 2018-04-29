# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ast
import json

from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View, TemplateView

from pis_product.models import Product
from pis_sales.models import SalesHistory
from pis_product.forms import PurchasedProductForm
from pis_sales.forms import BillingForm


class CreateBillingView(FormView):
    template_name = 'sales/create_invoice.html'
    form_class = BillingForm

    def get_context_data(self, **kwargs):
        context = super(CreateBillingView, self).get_context_data(**kwargs)
        products = self.request.user.retailer_user.retailer.retailer_product.all()
        context.update({
            'products': products
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


class CreateInvoiceView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateInvoiceView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        customer_name = self.request.POST.get('customer_name')
        customer_phone = self.request.POST.get('customer_phone')
        sub_total = self.request.POST.get('sub_total')
        discount = self.request.POST.get('discount')
        shipping = self.request.POST.get('shipping')
        grand_total = self.request.POST.get('grand_total')
        totalQty = self.request.POST.get('totalQty')
        items = json.loads(self.request.POST.get('items'))
        purchased_items_id = []

        for item in items:
            item_name = item.get('item_name')
            product = Product.objects.get(
                name=item_name,
                retailer=self.request.user.retailer_user.retailer
            )
            form_kwargs = {
                'product': product.id,
                'quantity': item.get('qty'),
                'discount_percentage': item.get('perdiscount'),
                'purchase_amount': item.get('total'),
            }
            form = PurchasedProductForm(form_kwargs)
            if form.is_valid():
                purchased_item = form.save()
                purchased_items_id.append(purchased_item.id)
                product_details = (
                    purchased_item.product.product_detail.
                    filter(available_item__gte=int(item.get('qty'))).first()
                )
                product_details.available_item = (
                    product_details.available_item - int(item.get('qty'))
                )
                product_details.purchased_item = (
                    product_details.purchased_item + int(item.get('qty')))
                product_details.save()

        billing_form_kwargs = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'sub_total': sub_total,
            'discount': discount,
            'grand_total': grand_total,
            'total_quantity': totalQty,
            'shipping': shipping,
            'purchased_items': purchased_items_id,
            'retailer': self.request.user.retailer_user.retailer.id,
        }

        billing_form = BillingForm(billing_form_kwargs)
        if billing_form.is_valid():
            invoice = billing_form.save()

        return JsonResponse({'invoice_id': invoice.id})


class InvoiceDetailView(TemplateView):
    template_name = 'sales/invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        invoice = SalesHistory.objects.get(id=self.kwargs.get('invoice_id'))
        context.update({
            'invoice': invoice,
            'product_details': invoice.product_details
        })
        return context


class InvoicesList(TemplateView):
    template_name = 'sales/invoice_list.html'

    @staticmethod
    def get_sales_history():
        return SalesHistory.objects.all()

    def get_context_data(self, **kwargs):
        context = super(InvoicesList, self).get_context_data(**kwargs)
        context.update({
            'invoices': self.get_sales_history(),
        })
        return context
