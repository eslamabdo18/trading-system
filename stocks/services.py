from datetime import datetime
# from dateutil import parser


class StockService:

    @staticmethod
    def update_stock_db(stock: dict) -> bool:
        from .models import Stock
        from dateutil import parser

        stock["timestamp"] = parser.parse(stock["timestamp"])
        obj, created = Stock.objects.update_or_create(
            stock_id=stock['stock_id'],
            defaults=stock
        )
