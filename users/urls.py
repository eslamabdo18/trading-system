from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from .views import UserViewset, DepositBalanceView, WithdrawBalanceView, BuyView, SellView, test

router = DefaultRouter()

router.register('users', UserViewset, "user-viewsets")

urlpatterns = router.urls


urlpatterns += [
    # ...
    path(r'users/<int:user_id>/deposit', DepositBalanceView.as_view()),
    path(r'users/<int:user_id>/withdraw', WithdrawBalanceView.as_view()),
    path(r'users/<int:user_id>/buy', BuyView.as_view()),
    path(r'users/<int:user_id>/sell', SellView.as_view()),
    path(r'users/test', test.as_view()),
    # ...
]
# urlpatterns += router.urls
