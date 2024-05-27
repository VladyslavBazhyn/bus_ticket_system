from rest_framework import viewsets, mixins

from station.models import Buss, Order
from station.serializers import BussSerializer, OrderSerializer


class BusViewSet(viewsets.ModelViewSet):
    queryset = Buss.objects.all()
    serializer_class = BussSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
