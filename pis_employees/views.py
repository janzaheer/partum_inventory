from django.views.generic import TemplateView, FormView, DeleteView, ListView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy

from pis_com.models import Customer
from pis_com.mixins import AuthRequiredMixin
from pis_employees.forms import EmployeeSalaryForm, EmployeeForm
from pis_employees.models import EmployeeSalary, Employee


class AddNewEmployee(AuthRequiredMixin, FormView):
    form_class = EmployeeForm
    template_name = "employee/create.html"

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('employee:employee_list'))

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


class EmployeeListView(AuthRequiredMixin, ListView):
    template_name = 'employee/employee_list.html'
    model = Employee
    paginate_by = 150

    def get_queryset(self):
        return Employee.objects.all().order_by('-date_of_joining')


class EmployeeDelete(AuthRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employee:employee_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class EmployeeSalaryView(AuthRequiredMixin, FormView):
    form_class = EmployeeSalaryForm
    template_name = 'employee/employee_salary.html'

    def form_valid(self, form):
        obj = form.save()
        try:
            obj.employee = Employee.objects.get(
                id=self.kwargs.get('pk'))
        except Employee.DoesNotExist:
            raise Http404('Employee not found')
        obj.save()
        return HttpResponseRedirect(reverse('employee:employee_list'))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            employee = Employee.objects.get(id=self.kwargs.get('pk'))
        except Employee.DoesNotExist:
            raise Http404('Employee not found')
        context.update({
            'employee': employee
        })
        return context


class EmployeeSalaryDetail(AuthRequiredMixin, TemplateView):
    template_name = 'employee/employee_salary_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            employee = Employee.objects.get(id=self.kwargs.get('pk'))
        except Employee.DoesNotExist:
            raise Http404('Employee not found')

        salaries = EmployeeSalary.objects.filter(
            employee=employee
        ).order_by('-date')

        context.update({
            'salaries': salaries,
            'employee': employee,
        })
        return context
