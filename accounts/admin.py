from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "currency")
    search_fields = ("user__username", "currency")
    list_filter = ("currency",)
