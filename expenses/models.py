from django.db import models
from accounts.models import Profile
from django.utils import timezone


class Wallet(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # type: ignore

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    CATEGORY_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES, default="expense")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon description ")
    color = models.CharField(max_length=20, blank=True, help_text="Color code")

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # type: ignore
    description = models.TextField("Transaction Description", blank=True)

    date = models.DateField("Transaction Date", default=timezone.now())
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.profile.user.username} | {self.wallet.name} | {self.category} | {self.amount}"

    @property
    def type(self):
        """Get transaction type (income or expense) from its category."""
        return self.category.type if self.category else "expense"

    @property
    def signed_amount(self):
        """Return positive for income, negative for expense."""
        return self.amount if self.type == "income" else -self.amount
