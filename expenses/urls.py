from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('transactions/', views.transactions_view, name="transactions"),
    path('accounts/', views.accounts_view, name="accounts"),
    path('add/', views.add_transaction, name="add_transaction"),
    path('add_wallet/', views.add_wallet, name="add_wallet")
] 