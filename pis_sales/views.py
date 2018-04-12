# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View, TemplateView

from pis_sales.forms import BillingForm


class CreateBillingView(FormView):
    template_name = 'sales/create_billing.html'
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
        return JsonResponse(request.POST)


class InvoiceDetailView(TemplateView):
    template_name = 'sales/invoice_detail.html'
