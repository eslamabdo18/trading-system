
from stocks.models import PendingOrders, Stock, UserStock
from users.models import User, UserTransaction
from django.shortcuts import get_object_or_404
from django.db import transaction


class OrderMatcher:

    def create_user_order(user_id, stock_id, cost, total_stocks):
        user = get_object_or_404(User, id=user_id)
        stock = get_object_or_404(Stock, stock_id=stock_id)
        user.balance -= cost
        user.save()
        user_stock = UserStock.objects.filter(user=user, stock=stock)
        if user_stock.exists():
            user_stock = user_stock.last()
            user_stock.total_count += total_stocks
            user_stock.buy_price += cost
            user_stock.save()
        else:
            UserStock.objects.create(
                user=user, stock=stock, buy_price=cost, total_count=total_stocks)
        UserTransaction.objects.create(
            user=user, stock=stock, type=UserTransaction.TranstionType.BUY, total_price=cost, total_count=total_stocks
        )

    @transaction.atomic
    def confirm_buy(stock: dict):
        pending_orders = PendingOrders.objects.select_for_update().filter(stock__name=stock['name'],
                                                                          order_type=PendingOrders.OrderType.BUY,
                                                                          upper_bound__gte=stock['price'], lower_bound__lte=stock['price'])

        for pending_order in pending_orders:
            total_stocks = min(pending_order.total, stock['availability'])
            cost = stock['price'] * total_stocks
            pending_order.total -= total_stocks
            OrderMatcher.create_user_order(
                pending_order.user_id, pending_order.stock.stock_id, cost, total_stocks)

            if pending_order.total == 0:
                pending_order.delete()
            else:
                pending_order.save()

            print("notify user")

    @transaction.atomic
    def confirm_sell(stock: dict):
        pending_orders = PendingOrders.objects.select_for_update().filter(stock__name=stock['name'],
                                                                          order_type=PendingOrders.OrderType.SELL,
                                                                          upper_bound__gte=stock['price'], lower_bound__lte=stock['price'])

        for pending_order in pending_orders:
            # total_stocks = min(pending_order.total, stock['availability'])
            cost = stock['price'] * pending_order.total
            user_stock = UserStock.objects.filter(
                user=pending_order.user, stock=pending_order.stock)
            if user_stock.exists():
                user_stock = user_stock.last()
                user_stock.total_count -= pending_order.total
                user_stock.buy_price -= cost
                user_stock.save()
                if user_stock.total_count == 0:
                    user_stock.delete()
                pending_order.user.balance += cost
                pending_order.user.save()
                pending_order.delete()

            print("notify sell user")
