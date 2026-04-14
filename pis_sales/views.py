import json

from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import FormView, DeleteView, View, TemplateView, ListView
from django.utils import timezone
from django.urls import reverse_lazy
from django.db import transaction

from pis_com.mixins import AuthRequiredMixin
from pis_product.models import Product, PurchasedProduct, StockOut
from pis_sales.models import SalesHistory
from pis_product.forms import PurchasedProductForm, ExtraItemForm, StockOutForm
from pis_sales.forms import BillingForm
from pis_com.forms import CustomerForm
from pis_com.models import Customer
from pis_ledger.models import Ledger
from pis_ledger.forms import LedgerForm


class CreateInvoiceView(AuthRequiredMixin, FormView):
    template_name = 'sales/create_invoice.html'
    form_class = BillingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = (
            self.request.user.retailer_user.retailer.retailer_product.all()
        )
        customers = (
            self.request.user.retailer_user.retailer.retailer_customer.all()
        )
        context.update({
            'products': products,
            'customers': customers,
            'present_date': timezone.now().date(),
        })
        return context


class ProductItemAPIView(AuthRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        retailer = self.request.user.retailer_user.retailer
        products = retailer.retailer_product.prefetch_related(
            'stockin_product', 'stockout_product'
        ).all()

        items = []
        for product in products:
            p = {
                'id': product.id,
                'name': product.name,
                'brand_name': product.brand_name,
            }

            stock_ins = list(product.stockin_product.all())
            if stock_ins:
                stock_detail = max(stock_ins, key=lambda s: s.id)
                p.update({
                    'retail_price': stock_detail.price_per_item,
                    'consumer_price': stock_detail.price_per_item,
                })

                all_stock = sum(s.quantity or 0 for s in stock_ins)
                purchased_stock = sum(
                    s.stock_out_quantity or 0
                    for s in product.stockout_product.all()
                )

                p.update({
                    'stock': float(all_stock - purchased_stock)
                })
            else:
                p.update({
                    'retail_price': 0,
                    'consumer_price': 0,
                })

            items.append(p)

        return JsonResponse({'products': items})


class GenerateInvoiceAPIView(AuthRequiredMixin, View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = None
        self.invoice = None

    def post(self, request, *args, **kwargs):
        customer_name = self.request.POST.get('customer_name')
        customer_phone = self.request.POST.get('customer_phone')
        discount = self.request.POST.get('discount')
        shipping = self.request.POST.get('shipping')
        grand_total = self.request.POST.get('grand_total')
        totalQty = self.request.POST.get('totalQty')
        remaining_payment = self.request.POST.get('remaining_amount')
        paid_amount = self.request.POST.get('paid_amount')
        cash_payment = self.request.POST.get('cash_payment')
        returned_cash = self.request.POST.get('returned_cash')

        try:
            items = json.loads(self.request.POST.get('items'))
        except (TypeError, json.JSONDecodeError):
            return JsonResponse(
                {'error': 'Invalid items data'}, status=400)

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
            if not billing_form.is_valid():
                return JsonResponse(
                    {'error': billing_form.errors}, status=400)
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
                            stock_out_form.save()

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

            self.invoice.purchased_items.set(purchased_items_id)
            self.invoice.extra_items.set(extra_items_id)
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
                        ledgerform.save()

            return JsonResponse({'invoice_id': self.invoice.id})


class InvoiceDetailView(AuthRequiredMixin, TemplateView):
    template_name = 'sales/invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            invoice = SalesHistory.objects.select_related(
                'retailer', 'customer'
            ).get(
                id=self.kwargs.get('invoice_id'),
                retailer=self.request.user.retailer_user.retailer,
            )
        except SalesHistory.DoesNotExist:
            from django.http import Http404
            raise Http404('Invoice not found')

        context.update({
            'invoice': invoice,
            'product_details': invoice.product_details,
            'extra_items_details': invoice.extra_items
        })
        return context


class InvoicesList(AuthRequiredMixin, ListView):
    template_name = 'sales/invoice_list.html'
    model = SalesHistory
    paginate_by = 200

    def get_queryset(self):
        return (
            self.request.user.retailer_user.retailer.
            retailer_sales.select_related('customer').all().order_by('-created_at')
        )


class UpdateInvoiceView(AuthRequiredMixin, FormView):
    template_name = 'sales/update_invoice.html'
    form_class = BillingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        retailer = self.request.user.retailer_user.retailer
        products = retailer.retailer_product.all()
        customers = retailer.retailer_customer.all()

        try:
            invoice = SalesHistory.objects.get(
                id=self.kwargs.get('id'),
                retailer=retailer,
            )
        except SalesHistory.DoesNotExist:
            from django.http import Http404
            raise Http404('Invoice not found')

        context.update({
            'products': products,
            'customers': customers,
            'present_date': timezone.now().date(),
            'invoice': invoice
        })
        return context


class UpdateInvoiceAPIView(AuthRequiredMixin, View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = None
        self.invoice = None

    def post(self, request, *args, **kwargs):
        discount = self.request.POST.get('discount')
        shipping = self.request.POST.get('shipping')
        grand_total = self.request.POST.get('grand_total')
        totalQty = self.request.POST.get('totalQty')
        remaining_payment = self.request.POST.get('remaining_amount')
        paid_amount = self.request.POST.get('paid_amount')
        invoice_id = self.request.POST.get('invoice_id')

        try:
            items = json.loads(self.request.POST.get('items'))
        except (TypeError, json.JSONDecodeError):
            return JsonResponse(
                {'error': 'Invalid items data'}, status=400)

        purchased_items_id = []
        extra_items_id = []
        retailer = self.request.user.retailer_user.retailer

        with transaction.atomic():
            for item in items:
                if item.get('item_id'):
                    purchased_item = PurchasedProduct.objects.get(
                        id=item.get('item_id'),
                    )

                    if purchased_item.quantity != item.get('qty'):
                        StockOut.objects.filter(
                            invoice__id=invoice_id,
                            stock_out_quantity='%g' % purchased_item.quantity,
                        ).delete()

                        purchased_item.price = item.get('price')
                        purchased_item.quantity = item.get('qty')
                        purchased_item.discount_percentage = item.get('perdiscount')
                        purchased_item.purchase_amount = item.get('total')
                        purchased_item.save()
                        purchased_items_id.append(purchased_item.id)

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

            invoice = SalesHistory.objects.get(id=invoice_id, retailer=retailer)
            invoice.discount = discount
            invoice.grand_total = grand_total
            invoice.total_quantity = totalQty
            invoice.shipping = shipping
            invoice.purchased_items.set(purchased_items_id)
            invoice.extra_items.set(extra_items_id)
            invoice.paid_amount = paid_amount
            invoice.remaining_payment = remaining_payment
            invoice.retailer = retailer

            if self.request.POST.get('customer_id'):
                invoice.customer = Customer.objects.get(
                    id=self.request.POST.get('customer_id'))

            invoice.save()

            if invoice.customer:
                try:
                    ledger = Ledger.objects.get(
                        customer__id=invoice.customer.id,
                        invoice__id=invoice.id
                    )
                    ledger.amount = remaining_payment
                    ledger.save()
                except Ledger.DoesNotExist:
                    pass
                except Ledger.MultipleObjectsReturned:
                    Ledger.objects.filter(
                        customer__id=invoice.customer.id,
                        invoice__id=invoice.id
                    ).update(amount=remaining_payment)

        return JsonResponse({'invoice_id': invoice.id})


class ProductDetailsAPIView(AuthRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            product_item = Product.objects.get(
                bar_code=self.request.POST.get('code'),
                retailer=self.request.user.retailer_user.retailer,
            )
        except Product.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'Item does not exist',
            })

        latest_stock = product_item.stockin_product.all().latest('id')

        all_stock = product_item.stockin_product.aggregate(
            total=Sum('quantity'))['total'] or 0
        purchased_stock = product_item.stockout_product.aggregate(
            total=Sum('stock_out_quantity'))['total'] or 0

        return JsonResponse({
            'status': True,
            'message': 'Success',
            'product_id': product_item.id,
            'product_name': product_item.name,
            'product_brand': product_item.brand_name,
            'product_price': '%g' % latest_stock.price_per_item,
            'stock': '%g' % (all_stock - purchased_stock)
        })


class SalesDeleteView(AuthRequiredMixin, DeleteView):
    model = SalesHistory
    success_url = reverse_lazy('sales:invoice_list')

    def get_queryset(self):
        return SalesHistory.objects.filter(
            retailer=self.request.user.retailer_user.retailer
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        PurchasedProduct.objects.filter(invoice__id=self.object.pk).delete()
        StockOut.objects.filter(invoice__id=self.object.pk).delete()
        Ledger.objects.filter(invoice__id=self.object.pk).delete()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
