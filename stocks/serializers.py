

from rest_framework import serializers
from .models import Stock, StockStream, UserStock


# class LimitedListSerializer(serializers.ListSerializer):

#     def to_representation(self, data):
#         data = data.all()[:100]
#         return super(FilteredListSerializer, self).to_representation(data)


class StockStreamSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StockStream
        fields = ['price', 'availability', 'timestamp']


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
    # last_prices = StockStreamSerializer(many=True, source="less_stream")
    last_prices = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ['stock_id', 'name', 'highest_price',
                  'lowest_price', 'average_price', 'last_prices']

    def get_last_prices(self, obj):
        return StockStreamSerializer(obj.less_stream(timestamp__range=self.context.get('filter')), many=True).data

    def get_highest_price(self, obj):
        print(self.context.get('filter'))
        if len(self.context.get('filter')) == 2:
            if not obj.highest_price(timestamp__range=self.context.get('filter'))['price__max']:
                raise Exception('enter valid range')
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


class UserStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStock
        fields = ['stock', 'total_count',]
