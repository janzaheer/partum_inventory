from __future__ import unicode_literals
from django.shortcuts import render

from django.views.generic import TemplateView, UpdateView
from django.views.generic import FormView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models import Sum
from pis_product.models import PurchasedProduct, ExtraItems, ClaimedProduct,StockOut, StockIn, Product
from pis_product.forms import (
    ProductForm, ProductDetailsForm, ClaimedProductForm,StockDetailsForm,StockOutForm)
from django.utils import timezone


class ProductItemList(TemplateView):
    template_name = 'products/product_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            ProductItemList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductItemList, self).get_context_data(**kwargs)
        products = (
            self.request.user.retailer_user.retailer.retailer_product.all()
        )
        context.update({
            'products': products
        })
        return context


class ProductDetailList(TemplateView):
    template_name = 'products/item_details.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            ProductDetailList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailList, self).get_context_data(**kwargs)
        try:
            product = (
                self.request.user.retailer_user.retailer.
                retailer_product.get(id=self.kwargs.get('pk'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found with concerned User')

        context.update({
            'items_details': product.product_detail.all().order_by(
                '-created_at'),
            'product': product,
        })

        return context


class AddNewProduct(FormView):
    form_class = ProductForm
    template_name = 'products/add_product.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            AddNewProduct, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product = form.save()

        return HttpResponseRedirect(reverse('product:stock_items_list'))

    def form_invalid(self, form):
        return super(AddNewProduct, self).form_invalid(form)


class AddProductItems(FormView):
    template_name = 'products/add_product_items.html'
    form_class = ProductDetailsForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(AddProductItems, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product_item_detail = form.save()
        return HttpResponseRedirect(
            reverse('product:item_details', kwargs={
                'pk': product_item_detail.product.id
            })
        )

    def form_invalid(self, form):
        return super(AddProductItems, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddProductItems, self).get_context_data(**kwargs)
        try:
            product = (
                self.request.user.retailer_user.retailer.
                retailer_product.get(id=self.kwargs.get('product_id'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found with concerned User')

        context.update({
            'product': product
        })
        return context


class PurchasedItems(TemplateView):
    template_name = 'products/purchased_items.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(PurchasedItems, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PurchasedItems, self).get_context_data(**kwargs)
        purchased_product = PurchasedProduct.objects.filter(
            product__retailer=self.request.user.retailer_user.retailer
        ).order_by('-created_at')

        context.update({
            'purchased_products': purchased_product
        })

        return context


class ExtraItemsView(TemplateView):
    template_name = 'products/purchased_extraitems.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(ExtraItemsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExtraItemsView, self).get_context_data(**kwargs)
        extra_products = ExtraItems.objects.filter(
            retailer=self.request.user.retailer_user.retailer
        )

        context.update({
            'purchased_extra_items': extra_products
        })

        return context


class ClaimedProductFormView(FormView):
    template_name = 'products/claimed_product.html'
    form_class = ClaimedProductForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            ClaimedProductFormView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def purchased_items_update(claimed_item, claimed_number):
        product = (
            claimed_item.product.product_detail.filter(
                available_item__gte=claimed_number
            ).first()
        )
        product.purchased_item = (
            product.purchased_item - claimed_number
        )
        product.save()

    # def claimed_items_payment(self, claimed_item, amount):
    #     payment_form_kwargs = {
    #         'customer': claimed_item.customer.id,
    #         'retailer': self.request.user.retailer_user.retailer.id,
    #         'amount': amount,
    #         'description': 'Amount Refunded from Claimed'
    #                        ' Item ID (%s)' % claimed_item.id
    #     }
    #     payment_form = PaymentForm(payment_form_kwargs)
    #     if payment_form.is_valid():
    #         payment_form.save()

    def form_valid(self, form):
        claimed_item = form.save()

        # update the purchased product accordingly
        self.purchased_items_update(
            claimed_item=claimed_item,
            claimed_number=int(form.cleaned_data.get('claimed_items'))
        )

        # Doing a payment of claimed amount
        # self.claimed_items_payment(
        #     claimed_item=claimed_item,
        #     amount=form.cleaned_data.get('claimed_amount')
        # )

        return HttpResponseRedirect(reverse('product:items_list'))
    
    def form_invalid(self, form):
        return super(ClaimedProductFormView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            ClaimedProductFormView, self).get_context_data(**kwargs)

        products = (
            self.request.user.retailer_user.retailer.
            retailer_product.all().order_by('name')
        )
        customers = (
            self.request.user.retailer_user.retailer.
            retailer_customer.all().order_by('customer_name')
        )
        context.update({
            'products': products,
            'customers': customers,
        })

        return context


class ClaimedItemsListView(TemplateView):
    template_name = 'products/claimed_product_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            ClaimedItemsListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            ClaimedItemsListView, self).get_context_data(**kwargs)
        context.update({
            'claimed_items': ClaimedProduct.objects.all().order_by(
                '-created_at')
        })
        return context


class StockItemList(ListView):
    template_name = 'products/stock_list.html'
    model = Product
    paginate_by = 150
    ordering = 'name'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            StockItemList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = (
                self.request.user.retailer_user.retailer
                    .retailer_product.all()
            )

        if self.request.GET.get('name'):
            queryset = queryset.filter(
                name__icontains=self.request.GET.get('name'))

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(StockItemList, self).get_context_data(**kwargs)
        context.update({
            'search_value_name': self.request.GET.get('name')
        })
        return context


class AddStockItems(FormView):
    template_name = 'products/add_stock_item.html'
    form_class = StockDetailsForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(AddStockItems, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product_item_detail = form.save()
        return HttpResponseRedirect(
            reverse('product:stock_items_list'
                    )
        )

    def form_invalid(self, form):
        return super(AddStockItems, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddStockItems, self).get_context_data(**kwargs)
        try:
            product = (
                self.request.user.retailer_user.retailer.
                retailer_product.get(id=self.kwargs.get('product_id'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found with concerned User')

        context.update({
            'product': product
        })
        return context


class StockOutItems(FormView):
    form_class = StockOutForm
    template_name = 'products/stock_out.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(StockOutItems, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product_item_detail = form.save()
        return HttpResponseRedirect(
            reverse('product:stock_items_list')
        )

    def form_invalid(self, form):
        return super(StockOutItems, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StockOutItems, self).get_context_data(**kwargs)
        try:
            product = (
                self.request.user.retailer_user.retailer.
                    retailer_product.get(id=self.kwargs.get('product_id'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found with concerned User')

        context.update({
            'product': product
        })
        return context


class StockDetailView(TemplateView):
    template_name = 'products/stock_detail.html'

    def get_context_data(self, **kwargs):
        context = super(
            StockDetailView, self).get_context_data(**kwargs)

        try:
            item = Product.objects.get(id=self.kwargs.get('product_id'))
        except StockIn.DoesNotExist:
            return Http404('Item does not exists in database')

        item_stocks_in = item.stockin_product.all()
        item_stocks_out = item.stockout_product.all()

        context.update({
            'item': item,
            'item_stock_in': item_stocks_in.order_by('-dated_order'),
            'item_stock_out': item_stocks_out.order_by('-dated'),
        })

        return context


class StockInListView(ListView):
    template_name = 'products/stockin_list.html'
    paginate_by = 100
    model = StockIn
    ordering = '-id'

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = StockIn.objects.all()

        queryset = queryset.filter(product=self.kwargs.get('product_id'))
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(StockInListView, self).get_context_data(**kwargs)
        context.update({
            'product': Product.objects.get(id=self.kwargs.get('product_id'))
        })
        return context


class StockOutListView(ListView):
    template_name = 'products/stockout_list.html'
    paginate_by = 100
    model = StockOut
    ordering = '-id'

    def get_queryset(self, **kwargs):
        queryset = self.queryset
        if not queryset:
            queryset = StockOut.objects.all()

        queryset = queryset.filter(product=self.kwargs.get('product_id'))
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(StockOutListView, self).get_context_data(**kwargs)
        context.update({
            'product': Product.objects.get(id=self.kwargs.get('product_id'))
        })
        return context


class ProductUpdateView(UpdateView):
    template_name = 'products/update_product.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:stock_items_list')


class StockInUpdateView(UpdateView):
    template_name = 'products/update_stockin.html'
    model = StockIn
    form_class = StockDetailsForm

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse('product:stockin_list',
                    kwargs={'product_id': obj.product.id})
        )
    
    def form_invalid(self, form):
        return super(StockInUpdateView, self).form_invalid(form)
