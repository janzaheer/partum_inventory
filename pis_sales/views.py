# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ast
import json
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DeleteView, View, TemplateView, ListView
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from pis_product.models import Product
from pis_sales.models import SalesHistory
from pis_product.forms import PurchasedProductForm
from pis_sales.forms import BillingForm
from pis_product.forms import ExtraItemForm, StockOutForm
from pis_com.forms import CustomerForm
from pis_ledger.models import Ledger
from pis_ledger.forms import LedgerForm
from django.db import transaction
from pis_product.models import PurchasedProduct, StockOut
from pis_com.models import Customer


class CreateInvoiceView(FormView):
    template_name = 'sales/create_invoice.html'
    form_class = BillingForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            CreateInvoiceView, self).dispatch(request, *args, **kwargs)

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
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            ProductItemAPIView, self).dispatch(request, *args, **kwargs)
    
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

            if product.stockin_product.exists():
                stock_detail = product.stockin_product.all().latest('id')
                p.update({
                    'retail_price': stock_detail.price_per_item,
                    'consumer_price': stock_detail.price_per_item,
                })

                all_stock = product.stockin_product.all()
                if all_stock:
                    all_stock = all_stock.aggregate(Sum('quantity'))
                    all_stock = float(all_stock.get('quantity__sum') or 0)
                else:
                    all_stock = 0

                purchased_stock = product.stockout_product.all()
                if purchased_stock:
                    purchased_stock = purchased_stock.aggregate(
                        Sum('stock_out_quantity'))
                    purchased_stock = float(
                        purchased_stock.get('stock_out_quantity__sum') or 0)
                else:
                    purchased_stock = 0

                p.update({
                    'stock': all_stock - purchased_stock
                })

            else:
                p.update(
                    {
                        'retail_price':0,
                        'consumer_price':0
                    }
                )

            items.append(p)

        return JsonResponse({'products': items})


class GenerateInvoiceAPIView(View):

    def __init__(self, *args, **kwargs):
        super(GenerateInvoiceAPIView, self).__init__(*args, **kwargs)
        self.customer = None
        self.invoice = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
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
        cash_payment = self.request.POST.get('cash_payment')
        returned_cash = self.request.POST.get('returned_cash')
        items = json.loads(self.request.POST.get('items'))
        purchased_items_id = []
        extra_items_id = []

        with transaction.atomic():

            billing_form_kwargs = {
                'discount': discount,
                'grand_total': grand_total,
                'total_quantity': totalQty,
                'shipping': shipping,
                'paid_amount': paid_amount,
                'remaining_payment': remaining_payment,
                'cash_payment': cash_payment,
                'returned_payment': returned_cash,
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
            self.invoice = billing_form.save()

            for item in items:
                item_name = item.get('item_name')
                try:
                    product = Product.objects.get(
                        name=item_name,
                        retailer=self.request.user.retailer_user.retailer
                    )
                    form_kwargs = {
                        'product': product.id,
                        'invoice': self.invoice.id,
                        'quantity': item.get('qty'),
                        'price': item.get('price'),
                        'discount_percentage': item.get('perdiscount'),
                        'purchase_amount': item.get('total'),
                    }
                    form = PurchasedProductForm(form_kwargs)
                    if form.is_valid():
                        purchased_item = form.save()
                        purchased_items_id.append(purchased_item.id)

                        latest_stock_in = (
                            product.stockin_product.all().latest('id'))

                        stock_out_form_kwargs = {
                            'product': product.id,
                            'invoice': self.invoice.id,
                            'purchased_item': purchased_item.id,
                            'stock_out_quantity': float(item.get('qty')),
                            'buying_price': (
                                float(latest_stock_in.buying_price_item) *
                                float(item.get('qty'))),
                            'selling_price': (
                                float(item.get('price')) * float(item.get('qty'))),
                            'dated': timezone.now().date()
                        }

                        stock_out_form = StockOutForm(stock_out_form_kwargs)
                        if stock_out_form.is_valid():
                            stock_out = stock_out_form.save()

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

            self.invoice.purchased_items = purchased_items_id
            self.invoice.extra_items = extra_items_id
            self.invoice.save()

            if self.customer or self.request.POST.get('customer_id'):
                if float(remaining_payment):
                    ledger_form_kwargs = {
                        'retailer': self.request.user.retailer_user.retailer.id,
                        'customer': (
                            self.request.POST.get('customer_id') or
                            self.customer.id),
                        'invoice': self.invoice.id,
                        'amount': remaining_payment,
                        'description': (
                            'Remaining Payment for Bill/Receipt No %s '
                            % self.invoice.receipt_no),
                        'dated': timezone.now()
                    }

                    ledgerform = LedgerForm(ledger_form_kwargs)
                    if ledgerform.is_valid():
                        ledger = ledgerform.save()

            return JsonResponse({'invoice_id': self.invoice.id})


class InvoiceDetailView(TemplateView):
    template_name = 'sales/invoice_detail.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            InvoiceDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        invoice = SalesHistory.objects.get(id=self.kwargs.get('invoice_id'))
        context.update({
            'invoice': invoice,
            'product_details': invoice.product_details,
            'extra_items_details': invoice.extra_items
        })
        return context


class InvoicesList(ListView):
    template_name = 'sales/invoice_list.html'
    model = SalesHistory
    paginate_by = 200
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(InvoicesList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = (
            self.request.user.retailer_user.retailer.
            retailer_sales.all().order_by('-created_at')
        )
        return queryset

    def get_sales_history(self):
        return (
            self.request.user.retailer_user.retailer.
            retailer_sales.all().order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super(InvoicesList, self).get_context_data(**kwargs)
        return context


class UpdateInvoiceView(FormView):
    template_name = 'sales/update_invoice.html'
    form_class = BillingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            UpdateInvoiceView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UpdateInvoiceView, self).get_context_data(**kwargs)
        products = (
            self.request.user.retailer_user.retailer.
                retailer_product.all()
        )
        customers = (
            self.request.user.retailer_user.
                retailer.retailer_customer.all()
        )
        invoice = SalesHistory.objects.get(id=self.kwargs.get('id'))
        context.update({
            'products': products,
            'customers': customers,
            'present_date': timezone.now().date(),
            'invoice': invoice
        })
        return context


class UpdateInvoiceAPIView(View):

    def __init__(self, *args, **kwargs):
        super(UpdateInvoiceAPIView, self).__init__(*args, **kwargs)
        self.customer = None
        self.invoice = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            UpdateInvoiceAPIView, self).dispatch(request, *args, **kwargs)

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
        invoice_id = self.request.POST.get('invoice_id')
        items = json.loads(self.request.POST.get('items'))
        purchased_items_id = []
        extra_items_id = []

        with transaction.atomic():
            for item in items:

                if item.get('item_id'):
                    # Getting Purchased Item by using Item ID or Invoice ID
                    # We are getting that by using Item ID
                    purchased_item = PurchasedProduct.objects.get(
                        id=item.get('item_id'),
                    )

                    # Delete the previous Stock Out Object,
                    # We need to create new one if quantity would not be same

                    if not purchased_item.quantity == item.get('qty'):
                        StockOut.objects.filter(
                            invoice__id=invoice_id,
                            stock_out_quantity='%g' % purchased_item.quantity,
                        ).delete()

                        # Update Purchased Product Details
                        purchased_item.price = item.get('price')
                        purchased_item.quantity = item.get('qty')
                        purchased_item.discount_percentage = item.get('perdiscount')
                        purchased_item.purchase_amount = item.get('total')
                        purchased_item.save()
                        purchased_items_id.append(purchased_item.id)

                        # Creating New stock iif quantity would get changed
                        stock_out_form_kwargs = {
                            'invoice': invoice_id,
                            'product': purchased_item.product.id,
                            'purchased_item': purchased_item.id,
                            'stock_out_quantity': item.get('qty'),
                            'dated': timezone.now().date()
                        }

                        stock_out_form = StockOutForm(stock_out_form_kwargs)
                        if stock_out_form.is_valid():
                            stock_out_form.save()

            invoice = SalesHistory.objects.get(id=invoice_id)
            invoice.discount = discount
            invoice.grand_total = grand_total
            invoice.total_quantity = totalQty
            invoice.shipping = shipping
            invoice.purchased_items = purchased_items_id
            invoice.extra_items = extra_items_id
            invoice.paid_amount = paid_amount
            invoice.remaining_payment = remaining_payment
            invoice.retailer = self.request.user.retailer_user.retailer

            if self.request.POST.get('customer_id'):
                invoice.customer = Customer.objects.get(
                    id=self.request.POST.get('customer_id'))

            invoice.save()

            if invoice.customer:
                ledger = Ledger.objects.get(
                    customer__id=invoice.customer.id,
                    invoice__id=invoice.id
                )
                ledger.amount = remaining_payment
                ledger.save()

        return JsonResponse({'invoice_id': invoice.id})


class ProductDetailsAPIView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            ProductDetailsAPIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            product_item = Product.objects.get(
                bar_code=self.request.POST.get('code'))
        except Product.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'Item with not exists',
            })

        latest_stock = product_item.stockin_product.all().latest('id')

        all_stock = product_item.stockin_product.all()
        if all_stock:
            all_stock = all_stock.aggregate(Sum('quantity'))
            all_stock = float(all_stock.get('quantity__sum') or 0)
        else:
            all_stock = 0

        purchased_stock = product_item.stockout_product.all()
        if purchased_stock:
            purchased_stock = purchased_stock.aggregate(
                Sum('stock_out_quantity'))
            purchased_stock = float(
                purchased_stock.get('stock_out_quantity__sum') or 0)
        else:
            purchased_stock = 0

        return JsonResponse({
            'status': True,
            'message': 'Success',
            'product_id': product_item.id,
            'product_name': product_item.name,
            'product_brand': product_item.brand_name,
            'product_price': '%g' % latest_stock.price_per_item,
            'stock': '%g' % (all_stock - purchased_stock)
        })


class SalesDeleteView(DeleteView):
    model = SalesHistory
    success_url = reverse_lazy('sales:invoice_list')

    def get(self, request, *args, **kwargs):
        PurchasedProduct.objects.filter(
            invoice__id=self.kwargs.get('pk')).delete()
        StockOut.objects.filter(
            invoice__id=self.kwargs.get('pk')).delete()
        Ledger.objects.filter(
            invoice__id=self.kwargs.get('pk')).delete()
        return self.delete(request, *args, **kwargs)
