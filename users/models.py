from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    balance = models.FloatField(default=0)


class UserTransaction(TimeStampMixin):
    class TranstionType(models.IntegerChoices):
        BUY = 1
        SELL = 2

    type = models.IntegerField(choices=TranstionType.choices)

    user = models.ForeignKey(
        User, related_name='transactions', on_delete=models.CASCADE)

    stock = models.ForeignKey(
        "stocks.Stock", related_name='stock_transtions', on_delete=models.CASCADE)

    total_price = models.FloatField()

    total_count = models.IntegerField()
