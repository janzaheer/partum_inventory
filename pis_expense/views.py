from django.views.generic import TemplateView, FormView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from pis_com.models import Customer
from pis_com.mixins import AuthRequiredMixin
from pis_expense.forms import ExtraExpenseForm
from pis_expense.models import ExtraExpense


class AddNewExpense(AuthRequiredMixin, FormView):
    form_class = ExtraExpenseForm
    template_name = 'expense/create_expense.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('expense:expense_list'))

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


class ExpenseListView(AuthRequiredMixin, TemplateView):
    template_name = 'expense/expense_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_list': ExtraExpense.objects.all().order_by('-date')
        })
        return context


class ExpenseDelete(AuthRequiredMixin, DeleteView):
    model = ExtraExpense
    success_url = reverse_lazy('expense:expense_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class dashboard(AuthRequiredMixin, TemplateView):
    template_name = 'expense/dashboard.html'
