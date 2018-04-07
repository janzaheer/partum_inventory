from django import forms

from pis_product.models import Product, ProductDetail


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "__all__"
