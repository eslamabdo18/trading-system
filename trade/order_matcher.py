
from stocks.models import PendingOrders, Stock, UserStock
from users.models import User, UserTransaction
from django.shortcuts import get_object_or_404
from django.db import transaction


class OrderMatcher:

    def create_user_order(user_id: int, stock_id: str, cost: float, total_stocks: int):

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

        # add the record into UserTransaction so we can track all the transactions and all the diffeernt priceces
        UserTransaction.objects.create(
            user=user, stock=stock, type=UserTransaction.TranstionType.BUY, total_price=cost, total_count=total_stocks
        )

    @transaction.atomic
    def confirm_operation(stock: dict, type: PendingOrders.OrderType):
        """
            params: stock: dict
            {
                "stock_id": "6ffb8e62-92c1-40c7-9d38-5b976a346b62",
                "name": "CIB",
                "price": 28,
                "availability": 46,
                "timestamp": "2019-12-15 14:36:33.462393"
            }
            description: this function run every time we receive an message
                         and check if we have any pending order that match the current stock
                         if yes we create order and add the stock to the user stocks

        """

        # get all the pendinng orders that match the current stock price
        # select for update is important just in case hhappend any duplicates
        pending_orders = PendingOrders.objects.select_for_update().filter(stock__name=stock['name'],
                                                                          order_type=type,
                                                                          upper_bound__gte=stock['price'], lower_bound__lte=stock['price'])

        for pending_order in pending_orders:
            if type == PendingOrders.OrderType.BUY:
                OrderMatcher.buy_order(pending_order, stock)
            else:
                OrderMatcher.sell_order(pending_order, stock)

    def buy_order(pending_order: PendingOrders, stock: dict):
        total_stocks = min(pending_order.total, stock['availability'])
        cost = stock['price'] * total_stocks
        pending_order.total -= total_stocks
        OrderMatcher.create_user_order(
            pending_order.user_id, pending_order.stock.stock_id, cost, total_stocks)

        if pending_order.total == 0:
            pending_order.delete()
        else:
            pending_order.save()

    def sell_order(pending_order: PendingOrders, stock: dict):
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

            UserTransaction.objects.create(
                user=pending_order.user, stock=pending_order.stock, type=UserTransaction.TranstionType.SELL, total_price=cost, total_count=pending_order.total
            )
