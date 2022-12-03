from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from .views import StockViewset

router = DefaultRouter()

router.register('stocks', StockViewset, "stocks-viewsets")
# router.register('stocks2', ProductList, "ProductList-viewsets")

urlpatterns = router.urls


# urlpatterns += [
#     # ...
#     # path(r'st2', ProductList.as_view()),

#     # ...
# ]
# urlpatterns += router.urls
