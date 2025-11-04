from django.db import models
from accounts.models import Profile
from django.utils import timezone
from datetime import timedelta


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

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField("Transaction Description", blank=True)

    is_recurring = models.BooleanField("Is Recurring", default=False)
    recurring_frequency = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
        ],
    )
    recurrence_end_date = models.DateField(
        blank=True,
        null=True,
        help_text="When the recurrence should stop (optional)",
    )

    date = models.DateField("Transaction Date", default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.profile.user.username} | {self.wallet.name} | {self.category} | {self.amount}"

    @property
    def type(self):
        return self.category.type if self.category else "expense"

    @property
    def signed_amount(self):
        return self.amount if self.type == "income" else -self.amount

    def get_next_occurrence(self):
        if not self.is_recurring or not self.recurring_frequency:
            return None
        delta_map = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "monthly": timedelta(days=30),
            "yearly": timedelta(days=365),
        }
        return self.date + delta_map.get(self.recurring_frequency, timedelta(days=0))
