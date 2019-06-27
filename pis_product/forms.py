from django import forms

from pis_product.models import (
    Product, ProductDetail, PurchasedProduct, ExtraItems, ClaimedProduct,
    StockIn,StockOut
)


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


class ClaimedProductForm(forms.ModelForm):
    class Meta:
        model = ClaimedProduct
        fields = "__all__"


class StockDetailsForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = "__all__"


class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = "__all__"