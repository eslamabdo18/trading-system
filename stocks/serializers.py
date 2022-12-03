

from rest_framework import serializers
from .models import Stock, StockStream


class StockStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockStream
        fields = ['price', 'availability']


class StockSerializer(serializers.ModelSerializer):
    highest_price = serializers.SerializerMethodField()
    lowest_price = serializers.SerializerMethodField()
    average_price = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ['stock_id', 'name', 'highest_price',
                  'lowest_price', 'average_price']

    def get_highest_price(self, obj):
        return obj.highest_price()['price__max']

    def get_lowest_price(self, obj):
        return obj.lowest_price()['price__min']

    def get_average_price(self, obj):
        return obj.get_avg_price()['price__avg']


class StockRetriveSerializer(serializers.ModelSerializer):
    highest_price = serializers.SerializerMethodField()
    lowest_price = serializers.SerializerMethodField()
    average_price = serializers.SerializerMethodField()
    stocks_stream = StockStreamSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['stock_id', 'name', 'highest_price',
                  'lowest_price', 'average_price', 'stocks_stream']

    def get_highest_price(self, obj):
        print(self.context.get('filter'))
        if len(self.context.get('filter')) == 2:
            return obj.highest_price(timestamp__range=self.context.get('filter'))['price__max']
        return obj.highest_price()['price__max']

    def get_lowest_price(self, obj):
        if len(self.context.get('filter')) == 2:
            return obj.lowest_price(timestamp__range=self.context.get('filter'))['price__min']
        return obj.lowest_price()['price__min']

    def get_average_price(self, obj):
        if len(self.context.get('filter')) == 2:
            return obj.get_avg_price(timestamp__range=self.context.get('filter'))['price__avg']
        return obj.get_avg_price()['price__avg']

    # def get_stream(self, obj):
    #     if len(self.context.get('filter')) == 2:
    #         query = obj.stocks_stream.filter(
    #             timestamp__range=self.context.get('filter')).all()[:20]
    #     query = obj.stocks_stream.filter(
    #         timestamp__range=self.context.get('filter')).all()[:20]
    #     return {"data": 0}
