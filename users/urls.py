from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from .views import UserViewset, DepositBalanceView, WithdrawBalanceView

router = DefaultRouter()

router.register('users', UserViewset, "user-viewsets")

urlpatterns = router.urls


urlpatterns += [
    # ...
    path(r'deposit', DepositBalanceView.as_view()),
    path(r'withdraw', WithdrawBalanceView.as_view()),
    # ...
]
# urlpatterns += router.urls
