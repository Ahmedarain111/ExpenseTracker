from django.contrib import admin
from django.urls import path, include

app_name = "expenses"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('expenses/', include('expenses.urls'))
]
