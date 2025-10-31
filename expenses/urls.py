from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('transactions/', views.transactions_view, name="transactions"),
    path('accounts/', views.accounts_view, name="accounts"),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('add_wallet/', views.add_wallet, name="add_wallet"),
    path("transactions/edit/<int:transaction_id>/", views.edit_transaction, name="edit_transaction"),
    path("transactions/delete/<int:transaction_id>/", views.delete_transaction, name="delete_transaction"),
    path("accounts/delete/<int:wallet_id>/", views.delete_wallet, name="delete_wallet"),
] 