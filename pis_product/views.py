from django.views.generic import TemplateView, UpdateView
from django.views.generic import FormView, ListView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from pis_com.mixins import AuthRequiredMixin
from pis_product.models import (
    PurchasedProduct, ExtraItems, ClaimedProduct, StockOut, StockIn, Product,
)
from pis_product.forms import (
    ProductForm, ProductDetailsForm, ClaimedProductForm,
    StockDetailsForm, StockOutForm,
)


class ProductItemList(AuthRequiredMixin, TemplateView):
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = (
            self.request.user.retailer_user.retailer.retailer_product.all()
        )
        context.update({
            'products': products
        })
        return context


class ProductDetailList(AuthRequiredMixin, TemplateView):
    template_name = 'products/item_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            product = (
                self.request.user.retailer_user.retailer.
                retailer_product.get(id=self.kwargs.get('pk'))
            )
        except ObjectDoesNotExist:
            raise Http404('Product not found with concerned User')

        context.update({
            'items_details': product.product_detail.all().order_by('-created_at'),
            'product': product,
        })
        return context


class AddNewProduct(AuthRequiredMixin, FormView):
    form_class = ProductForm
    template_name = 'products/add_product.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:stock_items_list'))

    def form_invalid(self, form):
        return super().form_invalid(form)


class AddProductItems(AuthRequiredMixin, FormView):
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
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class PurchasedItems(AuthRequiredMixin, TemplateView):
    template_name = 'products/purchased_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchased_product = PurchasedProduct.objects.filter(
            product__retailer=self.request.user.retailer_user.retailer
        ).select_related('product', 'invoice').order_by('-created_at')

        context.update({
            'purchased_products': purchased_product
        })
        return context


class ExtraItemsView(AuthRequiredMixin, TemplateView):
    template_name = 'products/purchased_extraitems.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_products = ExtraItems.objects.filter(
            retailer=self.request.user.retailer_user.retailer
        )
        context.update({
            'purchased_extra_items': extra_products
        })
        return context


class ClaimedProductFormView(AuthRequiredMixin, FormView):
    template_name = 'products/claimed_product.html'
    form_class = ClaimedProductForm

    @staticmethod
    def purchased_items_update(claimed_item, claimed_number):
        product = (
            claimed_item.product.product_detail.filter(
                available_item__gte=claimed_number
            ).first()
        )
        if product:
            product.purchased_item = (
                product.purchased_item - claimed_number
            )
            product.save()

    def form_valid(self, form):
        claimed_item = form.save()
        self.purchased_items_update(
            claimed_item=claimed_item,
            claimed_number=int(form.cleaned_data.get('claimed_items'))
        )
        return HttpResponseRedirect(reverse('product:items_list'))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class ClaimedItemsListView(AuthRequiredMixin, TemplateView):
    template_name = 'products/claimed_product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'claimed_items': ClaimedProduct.objects.filter(
                product__retailer=self.request.user.retailer_user.retailer
            ).select_related('product', 'customer').order_by('-created_at')
        })
        return context


class StockItemList(AuthRequiredMixin, ListView):
    template_name = 'products/stock_list.html'
    model = Product
    paginate_by = 150
    ordering = 'name'

    def get_queryset(self):
        queryset = (
            self.request.user.retailer_user.retailer
            .retailer_product.all()
        )

        if self.request.GET.get('name'):
            queryset = queryset.filter(
                name__icontains=self.request.GET.get('name'))

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_value_name': self.request.GET.get('name')
        })
        return context


class AddStockItems(AuthRequiredMixin, FormView):
    template_name = 'products/add_stock_item.html'
    form_class = StockDetailsForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:stock_items_list'))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class StockOutItems(AuthRequiredMixin, FormView):
    form_class = StockOutForm
    template_name = 'products/stock_out.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:stock_items_list'))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class StockDetailView(AuthRequiredMixin, TemplateView):
    template_name = 'products/stock_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            item = self.request.user.retailer_user.retailer.retailer_product.get(
                id=self.kwargs.get('product_id')
            )
        except Product.DoesNotExist:
            raise Http404('Item does not exist in database')

        context.update({
            'item': item,
            'item_stock_in': item.stockin_product.all().order_by('-dated_order'),
            'item_stock_out': item.stockout_product.select_related(
                'invoice'
            ).all().order_by('-dated'),
        })
        return context


class StockInListView(AuthRequiredMixin, ListView):
    template_name = 'products/stockin_list.html'
    paginate_by = 100
    model = StockIn
    ordering = '-id'

    def get_queryset(self):
        return StockIn.objects.filter(
            product__id=self.kwargs.get('product_id'),
            product__retailer=self.request.user.retailer_user.retailer,
        ).select_related('product').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            product = self.request.user.retailer_user.retailer.retailer_product.get(
                id=self.kwargs.get('product_id')
            )
        except Product.DoesNotExist:
            raise Http404('Product not found')
        context.update({'product': product})
        return context


class StockOutListView(AuthRequiredMixin, ListView):
    template_name = 'products/stockout_list.html'
    paginate_by = 100
    model = StockOut
    ordering = '-id'

    def get_queryset(self, **kwargs):
        return StockOut.objects.filter(
            product__id=self.kwargs.get('product_id'),
            product__retailer=self.request.user.retailer_user.retailer,
        ).select_related('product', 'invoice').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            product = self.request.user.retailer_user.retailer.retailer_product.get(
                id=self.kwargs.get('product_id')
            )
        except Product.DoesNotExist:
            raise Http404('Product not found')
        context.update({'product': product})
        return context


class ProductUpdateView(AuthRequiredMixin, UpdateView):
    template_name = 'products/update_product.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:stock_items_list')

    def get_queryset(self):
        return Product.objects.filter(
            retailer=self.request.user.retailer_user.retailer
        )


class StockInUpdateView(AuthRequiredMixin, UpdateView):
    template_name = 'products/update_stockin.html'
    model = StockIn
    form_class = StockDetailsForm

    def get_queryset(self):
        return StockIn.objects.filter(
            product__retailer=self.request.user.retailer_user.retailer
        )

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse('product:stockin_list',
                    kwargs={'product_id': obj.product.id})
        )

    def form_invalid(self, form):
        return super().form_invalid(form)
