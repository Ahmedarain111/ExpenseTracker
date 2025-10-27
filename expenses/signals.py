from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, Wallet
from django.db.models import Sum

@receiver(post_save, sender=Transaction)
def update_wallet_balance_on_save(sender, instance, created, **kwargs):
    """Recalculate wallet balance when a transaction is created or updated."""
    wallet = instance.wallet
    income_total = wallet.transactions.filter(category__type="income").aggregate(Sum("amount"))["amount__sum"] or 0
    expense_total = wallet.transactions.filter(category__type="expense").aggregate(Sum("amount"))["amount__sum"] or 0
    wallet.balance = income_total - expense_total
    wallet.save(update_fields=["balance"])


@receiver(post_delete, sender=Transaction)
def update_wallet_balance_on_delete(sender, instance, **kwargs):
    """Recalculate wallet balance when a transaction is deleted."""
    wallet = instance.wallet
    income_total = wallet.transactions.filter(category__type="income").aggregate(Sum("amount"))["amount__sum"] or 0
    expense_total = wallet.transactions.filter(category__type="expense").aggregate(Sum("amount"))["amount__sum"] or 0
    wallet.balance = income_total - expense_total
    wallet.save(update_fields=["balance"])
