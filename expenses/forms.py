from django import forms
from .models import Transaction, Wallet

from django import forms
from .models import Transaction
from .models import Wallet
from .models import Category


from django import forms
from .models import Transaction, Wallet

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "wallet",
            "category",
            "amount",
            "date",
            "description",
            "is_recurring",
            "recurring_frequency",
            "recurrence_end_date",
        ]

        widgets = {
            "wallet": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter amount"}
            ),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_recurring": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "recurring_frequency": forms.Select(
                attrs={"class": "form-select", "placeholder": "Select frequency"}
            ),
            "recurrence_end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)

        # Filter wallets by user profile
        if profile:
            self.fields["wallet"].queryset = Wallet.objects.filter(profile=profile)

        # Optional field rules
        self.fields["recurring_frequency"].required = False
        self.fields["recurrence_end_date"].required = False

        # Make sure non-recurring fields are required
        for field_name in ["wallet", "category", "amount", "date"]:
            self.fields[field_name].required = True

    def clean(self):
        """Ensure recurring fields are filled properly when is_recurring is True."""
        cleaned_data = super().clean()
        is_recurring = cleaned_data.get("is_recurring")
        frequency = cleaned_data.get("recurring_frequency")

        if is_recurring and not frequency:
            self.add_error("recurring_frequency", "Please select a recurring frequency.")

        return cleaned_data


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
