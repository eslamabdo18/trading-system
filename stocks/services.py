from .models import Stock, StockStream
from .models import Stock, StockStream

from dateutil import parser
import pytz
import time


class StockService:

    @staticmethod
    def update_stock_db(stock: dict) -> None:
        """
            params: stock: dict 
            {
                "stock_id": "6ffb8e62-92c1-40c7-9d38-5b976a346b62", 
                "name": "CIB", 
                "price": 28, 
                "availability": 46, 
                "timestamp": "2019-12-15 14:36:33.462393" 
            }
            description: this function recive stock(message) 
                         from the stram and insert it in the db
        """

        # convert the timestamp to datetime format
        timestamp = pytz.utc.localize(parser.parse(stock["timestamp"]))

        stock["timestamp"] = timestamp

        stock_obj, created = Stock.objects.update_or_create(
            name=stock['name'],
            defaults=stock
        )

        stream_obj = {"stock": stock_obj, "price": stock["price"],
                      "availability": stock["availability"], "timestamp": stock["timestamp"]}

        StockStream.objects.create(
            stock=stock_obj, price=stock["price"], availability=stock["availability"], timestamp=stock["timestamp"])
