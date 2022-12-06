from rest_framework import viewsets, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# from rest_framework import serializers


from .serializers import *
from .models import User
from trade.trade_service import TradeService

# Create your views here.


class UserViewset(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserRertiveSerializer
        return UserSerializer

    queryset = User.objects.all()
    serializer_class = UserSerializer


class DepositBalanceView(APIView):

    class InputSerializer(serializers.Serializer):
        amount = serializers.FloatField()

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data.get("amount")
        user = get_object_or_404(User, id=user_id)
        user.balance += amount
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class WithdrawBalanceView(APIView):

    class InputSerializer(serializers.Serializer):
        amount = serializers.FloatField()

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data.get("amount")
        user = get_object_or_404(User, id=user_id)
        if user.balance >= amount:
            user.balance -= amount
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"error": "you dont have the fund to withdraw"}, status=status.HTTP_400_BAD_REQUEST)


class BuyView(APIView):

    class InputSerializer(serializers.Serializer):
        stock_id = serializers.CharField()
        total = serializers.IntegerField()
        lower_bound = serializers.FloatField()
        upper_bound = serializers.FloatField()

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        TradeService.buy_stock(user_id, **serializer.validated_data)
        return Response({"message": "your order is being placed"}, status=status.HTTP_200_OK)


class test(APIView):

    # class InputSerializer(serializers.Serializer):
    #     stock_id = serializers.CharField()
    #     total = serializers.IntegerField()
    #     lower_bound = serializers.FloatField()
    #     upper_bound = serializers.FloatField()

    def get(self, request):
        from stocks.mqtt import Mqttclient
        Mqttclient().run()
        return Response({"message": "your order is being placed"}, status=status.HTTP_200_OK)


class SellView(APIView):

    class InputSerializer(serializers.Serializer):
        stock_id = serializers.CharField()
        total = serializers.IntegerField()
        lower_bound = serializers.FloatField()
        upper_bound = serializers.FloatField()

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        TradeService.sell_stock(user_id, **serializer.validated_data)
        return Response({"message": "your order is being placed"}, status=status.HTTP_200_OK)
