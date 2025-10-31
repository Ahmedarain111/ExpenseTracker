from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from .models import Profile
from expenses.models import Wallet, Transaction
from .forms import UserForm, ProfileForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)

            login(request, user)
            return redirect("expenses:dashboard")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("expenses:dashboard")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def profile_view(request):
    total_wallets = Wallet.objects.filter(profile=request.user.profile).count()
    total_transactions = Transaction.objects.filter(
        profile=request.user.profile
    ).count()
    total_expenses = (
        Transaction.objects.filter(profile=request.user.profile)
        .filter(category__type="expense")
        .count()
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "total_wallets": total_wallets,
            "total_transactions": total_transactions,
            "total_expenses": total_expenses,
        },
    )


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/edit_profile.html", {"form": form})
