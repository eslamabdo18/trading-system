from django.db import models

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
        ]

    def __str__(self):
        return self.name
