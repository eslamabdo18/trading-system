from .models import Stock, StockStream
from .models import Stock, StockStream

from dateutil import parser
import pytz
import time


class StockService:

    @staticmethod
    def update_stock_db(stock: dict) -> bool:

        # time.sleep(5)
        timestamp = pytz.utc.localize(parser.parse(stock["timestamp"]))
        # print(stock["name"], timestamp)
        stock["timestamp"] = timestamp

        stock_obj, created = Stock.objects.update_or_create(
            name=stock['name'],
            defaults=stock
        )

        stream_obj = {"stock": stock_obj, "price": stock["price"],
                      "availability": stock["availability"], "timestamp": stock["timestamp"]}

        # StockStream.objects.create(
        #     stock=stock_obj, price=stock["price"], availability=stock["availability"], timestamp=stock["timestamp"])
        obj, created = StockStream.objects.get_or_create(
            stock_id=stock_obj.id,
            price=stock["price"],
            availability=stock["availability"],
            timestamp=stock["timestamp"],
            defaults=stream_obj,
        )
