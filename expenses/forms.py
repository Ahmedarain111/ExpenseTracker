from django import forms
from .models import Transaction, Wallet

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["wallet", "category", "amount", "date", "description"]

        widgets = {
            "wallet": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter amount"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["name", "balance"]
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "balance": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter amount"}),
        }