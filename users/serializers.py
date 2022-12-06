from rest_framework import serializers
from .models import User
from stocks.serializers import UserStockSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', "balance", "password"]


class UserRertiveSerializer(serializers.ModelSerializer):
    stocks = UserStockSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'email', "balance", "stocks",]
