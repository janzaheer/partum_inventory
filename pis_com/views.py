# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.views.generic import TemplateView, RedirectView, UpdateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy

from pis_com.models import Customer
from pis_com.forms import CustomerForm

from pis_retailer.models import RetailerUser
from pis_retailer.forms import RetailerForm, RetailerUserForm


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


class RegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # register new user in the system
        user = form.save()

        # Create Retailer
        retailer_form_kwargs = {
            'name': (
                '%s %s' % (user.first_name, user.last_name) if
                user.first_name else user.username),
            'slug': (
                '%s-%s' % (user.first_name, user.last_name) if
                user.first_name else user.username)
        }
        retailer_form = RetailerForm(retailer_form_kwargs)
        if retailer_form.is_valid():
            retailer = retailer_form.save()

            retailer_user_kwargs = {
                'retailer': retailer.id,
                'user': user.id,
                'role_type': RetailerUser.ROLE_TYPE_LEDGER_VIEW
            }

            retailer_user_form = RetailerUserForm(retailer_user_kwargs)
            if retailer_user_form.is_valid():
                retailer_user_form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        auth_user = authenticate(username=username, password=raw_password)
        auth_login(self.request, auth_user)

        return HttpResponseRedirect(reverse('ledger:customer_ledger_list'))

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context.update({
                'username': self.request.POST.get('username'),
                'password1': self.request.POST.get('password1'),
                'password2': self.request.POST.get('password2')
            })

        return context


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

        customers = (
            self.request.user.retailer_user.retailer.
            retailer_customer.all().order_by('customer_name'))
        context.update({
            'customers': customers
        })
        return context


class CustomerUpdateView(UpdateView):
    form_class = CustomerForm
    template_name = 'customer/update_customer.html'
    model = Customer
