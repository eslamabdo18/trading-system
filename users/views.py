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
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DepositBalanceView(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        amount = serializers.FloatField()

    def put(self, request):
        print("hello")
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get("user_id")
        amount = serializer.validated_data.get("amount")
        user = get_object_or_404(User, id=user_id)
        user.balance += amount
        user.save()
        return Response(status=status.HTTP_200_OK)


class WithdrawBalanceView(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        amount = serializers.FloatField()

    def put(self, request):
        print("hello")
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get("user_id")
        amount = serializer.validated_data.get("amount")
        user = get_object_or_404(User, id=user_id)
        if user.balance >= amount:
            user.balance -= amount
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_304_NOT_MODIFIED)


class BuyView(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        stock_id = serializers.CharField()
        total = serializers.IntegerField()
        lower_bound = serializers.FloatField()
        upper_bound = serializers.FloatField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        TradeService.buy_stock(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class SellView(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        stock_id = serializers.CharField()
        total = serializers.IntegerField()
        lower_bound = serializers.FloatField()
        upper_bound = serializers.FloatField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        TradeService.buy_stock(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
