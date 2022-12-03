from django.contrib import admin

# Register your models here.

from .models import Stock, StockStream


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_id', 'price', 'name')


@admin.register(StockStream)
class StockStreamAdmin(admin.ModelAdmin):
    list_display = ('stock', 'price', 'timestamp')
