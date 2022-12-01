from django.contrib import admin

# Register your models here.

from .models import Stock


@admin.register(Stock)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('stock_id', 'price', 'name')
