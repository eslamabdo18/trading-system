from rest_framework import serializers
from .models import User, UserTransaction
from stocks.serializers import UserStockSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', "balance", "password"]
        read_only_fields = ('id',)


class UserTransactionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    stock_price = serializers.SerializerMethodField()

    def get_type(self, obj):
        types = {1: "Buy", 2: "Sell"}
        return types[obj.type]

    def get_stock(self, obj):
        return obj.stock.name

    def get_stock_price(self, obj):
        return obj.get_stock_price()

    class Meta:
        model = UserTransaction
        fields = ['stock', 'type', "stock_price", "total_price", "total_count"]


class UserRertiveSerializer(serializers.ModelSerializer):
    stocks = UserStockSerializer(many=True)
    recent_transactions = serializers.SerializerMethodField()

    def get_recent_transactions(self, obj):
        return UserTransactionSerializer(obj.transactions, many=True).data[:5]

    class Meta:
        model = User
        fields = ['username', 'email', "balance",
                  "stocks", 'recent_transactions']
