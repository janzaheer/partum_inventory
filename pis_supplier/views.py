from django.views.generic import UpdateView, FormView, ListView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import Sum

from pis_com.mixins import AuthRequiredMixin
from pis_supplier.models import Supplier, SupplierStatement
from pis_supplier.forms import SupplierForm, SupplierStatementForm


class AddSupplier(AuthRequiredMixin, FormView):
    form_class = SupplierForm
    template_name = 'supplier/add_supplier.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('supplier:list_supplier'))

    def form_invalid(self, form):
        return super().form_invalid(form)


class SupplierList(AuthRequiredMixin, ListView):
    template_name = 'supplier/list_supplier.html'
    model = Supplier
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier_statements = SupplierStatement.objects.all()
        try:
            supplier_amounts = supplier_statements.aggregate(Sum('supplier_amount'))
            supplier_amounts = supplier_amounts.get('supplier_amount__sum') or 0
            payment_amounts = supplier_statements.aggregate(Sum('payment_amount'))
            payment_amounts = payment_amounts.get('payment_amount__sum') or 0
        except (TypeError, ValueError):
            supplier_amounts = 0
            payment_amounts = 0

        total_remaining_amount = supplier_amounts - payment_amounts
        context.update({
            'total_remaining_amount': total_remaining_amount
        })
        return context


class SupplierStatementList(AuthRequiredMixin, ListView):
    template_name = 'supplier/list_supplier_statement.html'
    model = SupplierStatement
    paginate_by = 100

    def get_queryset(self):
        query_set = SupplierStatement.objects.filter(
            supplier__id=self.kwargs.get('pk')).order_by('-date')
        if self.request.GET.get('date'):
            query_set = query_set.filter(
                date=self.request.GET.get('date')
            )
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier_statements = SupplierStatement.objects.filter(supplier__id=self.kwargs.get('pk'))
        try:
            supplier = Supplier.objects.get(id=self.kwargs.get('pk'))
        except Supplier.DoesNotExist:
            raise Http404('Supplier not found')
        try:
            supplier_amounts = supplier_statements.aggregate(Sum('supplier_amount'))
            supplier_amounts = supplier_amounts.get('supplier_amount__sum') or 0
            payment_amounts = supplier_statements.aggregate(Sum('payment_amount'))
            payment_amounts = payment_amounts.get('payment_amount__sum') or 0
        except (TypeError, ValueError):
            supplier_amounts = 0
            payment_amounts = 0

        supplier_total_remaining_amount = supplier_amounts - payment_amounts

        context.update({
            'supplier': supplier,
            'supplier_total_remaining_amount': supplier_total_remaining_amount
        })
        return context


class AddSupplierStatement(AuthRequiredMixin, FormView):
    form_class = SupplierStatementForm
    template_name = 'supplier/add_supplier_statement.html'

    def form_valid(self, form):
        obj = form.save()
        try:
            obj.supplier = Supplier.objects.get(id=self.kwargs.get('pk'))
        except Supplier.DoesNotExist:
            raise Http404('Supplier not found')
        obj.save()
        return HttpResponseRedirect(reverse(
            'supplier:list_supplier_statement', kwargs={
                'pk': obj.supplier.id}))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            supplier = Supplier.objects.get(id=self.kwargs.get('pk'))
        except Supplier.DoesNotExist:
            raise Http404('Supplier not found')
        context.update({
            'supplier': supplier
        })
        return context


class SupplierStatementUpdate(AuthRequiredMixin, UpdateView):
    template_name = 'supplier/update_supplier_statement.html'
    model = SupplierStatement
    form_class = SupplierStatementForm

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse('supplier:list_supplier_statement', kwargs={'pk': obj.supplier.id})
        )

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statement = self.get_object()
        context.update({
            'supplier': statement.supplier
        })
        return context


class StatementPayment(AuthRequiredMixin, FormView):
    form_class = SupplierStatementForm
    template_name = 'supplier/payment.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse(
            'supplier:list_supplier_statement', kwargs={
                'pk': self.kwargs.get('pk')}))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            supplier = Supplier.objects.get(id=self.kwargs.get('pk'))
        except Supplier.DoesNotExist:
            raise Http404('Supplier not found')
        context.update({
            'supplier': supplier
        })
        return context
