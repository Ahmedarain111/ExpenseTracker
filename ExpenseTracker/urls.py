from django.contrib import admin
from django.urls import path, include
from expenses.views import home_view

app_name = "expenses"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_view, name="home"),
    path('accounts/', include('accounts.urls')),
    path('expenses/', include('expenses.urls'))
]
