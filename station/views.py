from rest_framework import viewsets

from station.models import Buss, Trip, Facility, Order
from station.serializers import (
    BussListSerializer,
    TripSerializer,
    TripListSerializer,
    BussSerializer,
    FacilitySerializer,
    BussRetrieveSerializer,
    TripRetrieveSerializer,
    OrderSerializer
)


class BusViewSet(viewsets.ModelViewSet):
    queryset = Buss.objects.all()
    serializer_class = BussSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BussListSerializer
        elif self.action == "retrieve":
            return BussRetrieveSerializer

        return BussSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ["list", "retrieve"]:
            return queryset.prefetch_related("facilities").filter(user=self.request.user.id)
        return queryset.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(self.request.user)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        elif self.action == "retrieve":
            return TripRetrieveSerializer

        return TripSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ["list", "retrieve"]:
            return queryset.select_related()
        return self.queryset


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
