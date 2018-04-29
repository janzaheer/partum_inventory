from django import forms

from pis_sales.models import SalesHistory, Customer


class BillingForm(forms.ModelForm):
    class Meta:
        model = SalesHistory
        fields = "__all__"


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
