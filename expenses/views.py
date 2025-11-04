import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transaction, Wallet, Category
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .forms import TransactionForm, WalletForm
from django.db.models import Sum
from datetime import date
import calendar, json
from datetime import timedelta


def home_view(request):
    return render(request, "home.html")


@login_required
def dashboard_view(request):
    profile = request.user.profile
    today = date.today()
    current_month = today.month
    current_year = today.year

    user_wallets = Wallet.objects.filter(profile=profile)
    user_transactions = Transaction.objects.filter(profile=profile)

    total_balance = user_wallets.aggregate(total=Sum("balance"))["total"] or 0
    total_income = (
        user_transactions.filter(
            category__type="income",
            date__month=current_month,
            date__year=current_year,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )
    total_expenses = (
        user_transactions.filter(
            category__type="expense",
            date__month=current_month,
            date__year=current_year,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    savings = total_income - total_expenses

    months, income_data, expense_data = [], [], []
    for i in range(5, -1, -1):
        month_num = (current_month - i - 1) % 12 + 1
        year = current_year if current_month - i > 0 else current_year - 1
        month_name = calendar.month_abbr[month_num]
        months.append(month_name)

        income_sum = (
            user_transactions.filter(
                category__type="income", date__month=month_num, date__year=year
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
        expense_sum = (
            user_transactions.filter(
                category__type="expense", date__month=month_num, date__year=year
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        income_data.append(float(income_sum))
        expense_data.append(float(expense_sum))

    category_labels, category_values = [], []
    categories = Category.objects.filter(type="expense")

    for cat in categories:
        spent = (
            user_transactions.filter(
                category=cat,
                date__month=current_month,
                date__year=current_year,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
        if spent > 0:
            category_labels.append(cat.name)
            category_values.append(float(spent))

    recent_transactions = user_transactions.order_by("-date")[:10]

    context = {
        "total_balance": total_balance,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings,
        "months": json.dumps(months),
        "income_data": json.dumps(income_data),
        "expense_data": json.dumps(expense_data),
        "category_labels": json.dumps(category_labels),
        "category_values": json.dumps(category_values),
        "recent_transactions": recent_transactions,
    }

    return render(request, "expenses/dashboard.html", context)


def transactions_view(request):
    profile = request.user.profile
    today = date.today()

    transactions = Transaction.objects.filter(profile=profile, date__lte=today)
    wallets = Wallet.objects.filter(profile=profile)

    wallet_id = request.GET.get("wallet")
    sort_option = request.GET.get("sort")

    if wallet_id:
        transactions = transactions.filter(wallet_id=wallet_id)

    if sort_option == "amount_asc":
        transactions = transactions.order_by("amount")
    elif sort_option == "amount_desc":
        transactions = transactions.order_by("-amount")
    elif sort_option == "date_asc":
        transactions = transactions.order_by("date")
    elif sort_option == "date_desc":
        transactions = transactions.order_by("-date")
    else:
        transactions = transactions.order_by("-date", "-created_at")

    return render(
        request,
        "expenses/transactions.html",
        {"transactions": transactions, "wallets": wallets},
    )


@login_required
def accounts_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    wallets = Wallet.objects.filter(profile=profile)

    return render(request, "expenses/accounts.html", {"wallets": wallets})


from django.shortcuts import render, redirect
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required


@login_required
def add_transaction(request):
    profile = request.user.profile

    if request.method == "POST":
        form = TransactionForm(request.POST, profile=profile)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.profile = profile
            transaction.save()

            if transaction.is_recurring and transaction.recurring_frequency:
                next_date = transaction.get_next_occurrence()
                end_date = transaction.recurrence_end_date

                while next_date and (not end_date or next_date <= end_date):
                    Transaction.objects.create(
                        profile=profile,
                        wallet=transaction.wallet,
                        category=transaction.category,
                        amount=transaction.amount,
                        description=f"(Recurring) {transaction.description}",
                        is_recurring=False,
                        date=next_date,
                    )
                    next_date += {
                        "daily": timedelta(days=1),
                        "weekly": timedelta(weeks=1),
                        "monthly": timedelta(days=30),
                        "yearly": timedelta(days=365),
                    }.get(transaction.recurring_frequency, timedelta(days=0))

            messages.success(request, "Transaction added successfully!")
            return redirect("expenses:transactions")
    else:
        form = TransactionForm(profile=profile)

    return render(request, "expenses/add_transaction.html", {"form": form})


@login_required
def add_wallet(request):
    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.profile = request.user.profile
            wallet.save()
            return redirect("expenses:accounts")
    else:
        form = WalletForm()

    return render(request, "expenses/add_wallet.html", {"form": form})


def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction, id=transaction_id, profile=request.user.profile
    )

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully!")
            return redirect("expenses:transactions")
    else:
        form = TransactionForm(instance=transaction)

    return render(
        request,
        "expenses/edit_transaction.html",
        {"form": form, "transaction": transaction},
    )


def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction, id=transaction_id, profile=request.user.profile
    )

    if request.method == "POST":
        transaction.delete()
        messages.success(request, "Transaction deleted successfully!")
        return redirect("expenses:transactions")

    return render(request, "expenses/confirm_delete.html", {"transaction": transaction})


def delete_wallet(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, profile=request.user.profile)

    if request.method == "POST":
        wallet.delete()
        messages.success(request, "Wallet deleted successfully!")
        return redirect("expenses:accounts")

    return render(request, "expenses/confirm_wallet_delete.html", {"wallet": wallet})
