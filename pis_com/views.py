# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView, RedirectView, UpdateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy

from pis_com.models import Customer
from pis_com.forms import CustomerForm


class LoginView(FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm
    
    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(reverse('index'))
    
    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context


class LogoutView(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        auth_logout(self.request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('login'))


class HomePageView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        else:

            if self.request.user.retailer_user:
                if (
                    self.request.user.retailer_user.role_type ==
                        self.request.user.retailer_user.ROLE_TYPE_SALESMAN
                ):
                    return HttpResponseRedirect(reverse('sales:invoice_list'))
            if self.request.user.retailer_user:
                if (
                        self.request.user.retailer_user.role_type ==
                        self.request.user.retailer_user.ROLE_TYPE_DATA_ENTRY_USER
                ):
                    return HttpResponseRedirect(reverse('product:items_list'))

        return super(
            HomePageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


class CreateCustomer(FormView):
    form_class = CustomerForm
    template_name = 'customer/create_customer.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('customers'))
    
    def form_invalid(self, form):
        return super(CreateCustomer, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            CreateCustomer, self).get_context_data(**kwargs)

        customers = Customer.objects.all()
        context.update({
            'customers': customers
        })
        return context


class CustomerTemplateView(TemplateView):
    template_name = 'customer/customer_list.html'

    def get_context_data(self, **kwargs):
        context = super(
            CustomerTemplateView, self).get_context_data(**kwargs)

        customers = Customer.objects.all().order_by('customer_name')
        context.update({
            'customers': customers
        })
        return context


class CustomerUpdateView(UpdateView):
    form_class = CustomerForm
    template_name = 'customer/update_customer.html'
    model = Customer
