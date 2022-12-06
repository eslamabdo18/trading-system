

from rest_framework import serializers
from .models import Stock, StockStream, UserStock
from users.serializers import UserTransaction


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


class StockTransactionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    stock_price = serializers.SerializerMethodField()

    def get_type(self, obj):
        types = {1: "Buy", 2: "Sell"}
        return types[obj.type]

    def get_stock_price(self, obj):
        return obj.get_stock_price()

    class Meta:
        model = UserTransaction
        fields = ['user', 'type', "stock_price",
                  "total_price", "total_count"]


class StockRetriveSerializer(serializers.ModelSerializer):
    highest_price = serializers.SerializerMethodField()
    lowest_price = serializers.SerializerMethodField()
    average_price = serializers.SerializerMethodField()
    recent_data = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ['stock_id', 'name', 'highest_price',
                  'lowest_price', 'average_price', 'recent_data', 'transactions']

    def get_recent_data(self, obj):
        if len(self.context.get('filter')) == 2:
            return StockStreamSerializer(obj.less_stream(timestamp__range=self.context.get('filter')), many=True).data
        return StockStreamSerializer(obj.less_stream(), many=True).data

    def get_transactions(self, obj):
        if len(self.context.get('filter')) == 2:
            return StockTransactionSerializer(obj.less_stock_transtions(created_at__range=self.context.get('filter')), many=True).data
        return StockTransactionSerializer(obj.less_stock_transtions(), many=True).data

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


class StockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['stock_id', 'name']


class UserStockSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source="stock")
    stock_id = serializers.SerializerMethodField()

    def get_stock_id(self, obj):
        return obj.stock.stock_id

    class Meta:
        model = UserStock
        fields = ['stock_id', 'name', 'total_count']
