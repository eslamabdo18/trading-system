from dateutil import parser
import pytz
from rest_framework import viewsets, generics
import django_filters
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend
from rest_framework.response import Response
# from rest_framework import generics


from .serializers import StockSerializer, StockRetriveSerializer
from .models import Stock


class ProductFilter(django_filters.FilterSet):
    from_date = django_filters.DateTimeFilter(
        name="timestamp", lookup_type='gte')
    to_date = django_filters.DateTimeFilter(
        name="timestamp", lookup_type='lte')

    class Meta:
        model = Stock
        fields = ['from_date', 'to_date']


class StockViewset(viewsets.ReadOnlyModelViewSet):

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StockRetriveSerializer
        return StockSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        filter_date = []
        if "from_date" in self.request.query_params and "to_date" in self.request.query_params:
            from_date = pytz.utc.localize(parser.parse(
                self.request.query_params['from_date']))
            to_date = pytz.utc.localize(parser.parse(
                self.request.query_params['to_date']))
            filter_date.append(from_date)
            filter_date.append(to_date)
        context["query_params"] = self.request.query_params
        context['filter'] = filter_date
        return context

    queryset = Stock.objects.all().prefetch_related("stocks_stream")
    serializer_class = StockSerializer
    lookup_field = "stock_id"

# class ProductList(generics.ListAPIView):
#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer
#     filterset_class = ProductFilter
