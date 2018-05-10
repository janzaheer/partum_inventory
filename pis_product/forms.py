from django import forms

from pis_product.models import (
    Product, ProductDetail, PurchasedProduct, ExtraItems)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "__all__"


class PurchasedProductForm(forms.ModelForm):
    class Meta:
        model = PurchasedProduct
        fields = "__all__"


class ExtraItemForm(forms.ModelForm):
    class Meta:
        model = ExtraItems
        fields = "__all__"

