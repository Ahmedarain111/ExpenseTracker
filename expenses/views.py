from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transaction, Wallet
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .forms import TransactionForm, WalletForm

def home_view(request):
    return render(request, 'home.html')



@login_required
def dashboard_view(request):
    return render(request, "expenses/dashboard.html")

@login_required
def transactions_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    user_transactions = Transaction.objects.filter(profile=profile).select_related("wallet", "category")

    return render(request, "expenses/transactions.html", {
        "transactions": user_transactions,
    })

@login_required
def accounts_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    wallets = Wallet.objects.filter(profile=profile)
    
    return render(request, "expenses/accounts.html", {"wallets": wallets})

@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.profile = request.user.profile  # link transaction to logged-in user
            transaction.save()
            return redirect("expenses:transactions")
    else:
        form = TransactionForm()

    return render(request, "expenses/add_transaction.html", {"form": form})

@login_required
def add_wallet(request):
    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.profile = request.user.profile
            wallet.save()
            return  redirect("expenses:accounts")
    else:
        form = WalletForm()
        
    return render(request, "expenses/add_wallet.html", {"form": form})

def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, profile=request.user.profile)
    
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully!")
            return redirect("expenses:transactions")
    else:
        form = TransactionForm(instance=transaction)

    return render(request, "expenses/edit_transaction.html", {"form": form, "transaction": transaction})


def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, profile=request.user.profile)

    if request.method == "POST":
        transaction.delete()
        messages.success(request, "Transaction deleted successfully!")
        return redirect("expenses:transactions")

    return render(request, "expenses/confirm_delete.html", {"transaction": transaction})