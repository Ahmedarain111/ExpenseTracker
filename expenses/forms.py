from django import forms
from .models import Transaction, Wallet

from django import forms
from .models import Transaction
from .models import Wallet
from .models import Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["wallet", "category", "amount", "date", "description"]

        widgets = {
            "wallet": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter amount"}
            ),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)

        if profile:
            self.fields["wallet"].queryset = Wallet.objects.filter(profile=profile)

        for field_name, field in self.fields.items():
            if field_name != "description":
                field.required = True


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["name", "balance"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "balance": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter amount"}
            ),
        }
