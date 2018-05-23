from django import forms

from pis_ledger.models import Ledger, PaymentLedger


class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = "__all__"


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentLedger
        fields = '__all__'

