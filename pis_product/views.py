from __future__ import unicode_literals
from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from pis_product.models import PurchasedProduct, ExtraItems
from pis_product.forms import ProductForm, ProductDetailsForm


class ProductItemList(TemplateView):
    template_name = 'products/product_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('login'))

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
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('login'))

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
            'items_details': product.product_detail.all(),
            'product': product,
        })

        return context


class AddNewProduct(FormView):
    form_class = ProductForm
    template_name = 'products/add_product.html'

    @staticmethod
    def add_product_details(product_id, details_form_kwargs):
        form_kwargs = {
            'product': product_id,
        }
        form_kwargs.update(details_form_kwargs)
        form = ProductDetailsForm(form_kwargs)
        if form.is_valid():
            form.save()
        else:
            return
        return form

    def form_valid(self, form):
        product = form.save()
        details_form_kwargs = {
            'retail_price': self.request.POST.get('retail_price'),
            'consumer_price': self.request.POST.get('consumer_price'),
            'available_item': self.request.POST.get('available_item'),
            'purchased_item': self.request.POST.get('purchased_item'),
        }
        self.add_product_details(
            product_id=product.id,
            details_form_kwargs=details_form_kwargs
        )

        return HttpResponseRedirect(reverse('product:items_list'))

    def form_invalid(self, form):
        return super(AddNewProduct, self).form_invalid(form)


class AddProductItems(FormView):
    template_name = 'products/add_product_items.html'
    form_class = ProductDetailsForm

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

    def get_context_data(self, **kwargs):
        context = super(PurchasedItems, self).get_context_data(**kwargs)
        purchased_product = PurchasedProduct.objects.filter(
            product__retailer=self.request.user.retailer_user.retailer
        )

        context.update({
            'purchased_products': purchased_product
        })

        return context


class ExtraItemsView(TemplateView):
    template_name = 'products/purchased_extraitems.html'

    def get_context_data(self, **kwargs):
        context = super(ExtraItemsView, self).get_context_data(**kwargs)
        extra_products = ExtraItems.objects.filter(
            retailer=self.request.user.retailer_user.retailer
        )

        context.update({
            'purchased_extra_items': extra_products
        })

        return context