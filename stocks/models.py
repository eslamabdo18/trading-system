from django.db import models
from django.db.models import Max, Min, Avg

# Create your models here.


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Stock(TimeStampMixin):
    stock_id = models.CharField(max_length=500, unique=True)
    name = models.CharField(max_length=150, unique=True)
    price = models.FloatField()
    availability = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['stock_id', ]),
            models.Index(fields=['name', ]),
        ]

    def highest_price(self, *args, **kwargs):
        print(kwargs)
        print(args)
        stream_stocks = self.stocks_stream.filter(
            **kwargs).prefetch_related("stocks_stream")
        return stream_stocks.aggregate(Max('price'))

    def lowest_price(self, *args, **kwargs):
        stream_stocks = self.stocks_stream.filter(
            **kwargs).prefetch_related("stocks_stream")
        return stream_stocks.aggregate(Min('price'))

    def get_avg_price(self, *args, **kwargs):
        stream_stocks = self.stocks_stream.filter(
            **kwargs).prefetch_related("stocks_stream")
        return stream_stocks.aggregate(Avg('price'))

    def __str__(self):
        return self.name


class StockStream(TimeStampMixin):
    stock = models.ForeignKey(
        Stock, related_name='stocks_stream', on_delete=models.CASCADE)
    price = models.FloatField()
    availability = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['stock_id', 'timestamp']),
        ]


class UserStock(TimeStampMixin):
    user = models.ForeignKey(
        "users.User", related_name='stocks', on_delete=models.CASCADE)

    stock = models.ForeignKey(
        Stock, related_name='users_stock', on_delete=models.CASCADE)

    buy_price = models.FloatField()

    total_count = models.FloatField()


class PendingOrders(TimeStampMixin):
    class OrderType(models.IntegerChoices):
        BUY = 1
        SELL = 2

    user = models.ForeignKey(
        "users.User", related_name='pending_stocks', on_delete=models.CASCADE)

    stock = models.ForeignKey(
        Stock, related_name='users_pending_stock', on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=OrderType.choices)
    total = models.IntegerField()
    upper_bound = models.FloatField()
    lower_bound = models.FloatField()
