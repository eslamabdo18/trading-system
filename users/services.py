
from django.shortcuts import get_object_or_404

from .models import User


class TradeService:
    pass

    # def _validate_user_funds(user_id: int, total: int, upper_bound: float):
    #     user = get_object_or_404(User, id=user_id)
    #     if total * upper_bound > user.balance:
    #         raise Exception("insufficient amount")

    # def buy_stock(user_id: int, stock_id: str, total: int, lower_bound: int, upper_bound: int):
    #     user = get_object_or_404(User, id=user_id)
    #     stock = get_object_or_404(Stock, stock_id=stock_id)
