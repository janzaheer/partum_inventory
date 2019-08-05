from django import forms
from pis_supplier.models import Supplier, SupplierStatement

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class SupplierStatementForm(forms.ModelForm):
    class Meta:
        model = SupplierStatement
        fields = '__all__'
