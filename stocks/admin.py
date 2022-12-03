from django.contrib import admin

# Register your models here.

from .models import Stock, StockStream, UserStock, PendingOrders


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_id', 'price', 'name')


@admin.register(StockStream)
class StockStreamAdmin(admin.ModelAdmin):
    list_display = ('stock', 'price', 'timestamp')


@admin.register(UserStock)
class UserStockAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'buy_price')


@admin.register(PendingOrders)
class PendingOrdersAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'total')
