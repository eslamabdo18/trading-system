
from django.shortcuts import get_object_or_404
from django.core.exceptions import SuspiciousOperation

from users.models import User
from stocks.models import Stock, UserStock, PendingOrders


class TradeService:

    def _validate_order(user: User, total: int, upper_bound: float, stock: Stock) -> bool:
        if total * upper_bound > user.balance:
            raise SuspiciousOperation(
                "insufficient amount, please deposit money so you can place order")

    def create_user_order(user: User, stock: Stock):
        user.balance -= stock.price
        user.save()
        UserStock.objects.create(user=user, stock=stock, buy_price=stock.price)

    def create_pending_order(*args, **kwrgs):
        PendingOrders.objects.create(**kwrgs)

    def buy_stock(user_id: int, stock_id: str, total: int, lower_bound: int, upper_bound: int):
        user = get_object_or_404(User, id=user_id)
        stock = get_object_or_404(Stock, stock_id=stock_id)

        # raise excption if the user dosent have the money to buy
        TradeService._validate_order(user, total, upper_bound, stock)
        # # else the order will be pending till the order engine matcher match with the user price again
        TradeService.create_pending_order(
            user_id=user_id, stock=stock, order_type=PendingOrders.OrderType.BUY, total=total, upper_bound=upper_bound, lower_bound=lower_bound)

        return "Your order is being placed"

    def sell_stock(user_id: int, stock_id: str, total: int, lower_bound: int, upper_bound: int):
        user = get_object_or_404(User, id=user_id)
        stock = get_object_or_404(Stock, stock_id=stock_id)

        user_stocks = user.stocks.filter(id=stock.id)
        if not user_stocks.exists():
            raise Exception(
                "you dont have this stock to sell it")
        if user_stocks.last().total_count < total:
            raise Exception(
                "you cant sell because you dont have this amount")
        # # else the order will be pending till the order engine matcher match with the user price again
        TradeService.create_pending_order(
            user_id=user_id, stock=stock, order_type=PendingOrders.OrderType.SELL, total=total, upper_bound=upper_bound, lower_bound=lower_bound)

        return "Your order is being placed"
