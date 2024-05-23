from rest_framework import viewsets

from station.models import Buss, Trip, Facility
from station.serializers import (
    BussListSerializer,
    TripSerializer,
    TripListSerializer,
    BussSerializer,
    FacilitySerializer,
    BussRetrieveSerializer,
    TripRetrieveSerializer
)


class BusViewSet(viewsets.ModelViewSet):
    queryset = Buss.objects.all()
    serializer_class = BussListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BussListSerializer
        elif self.action == "retrieve":
            return BussRetrieveSerializer

        return BussSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ["list", "retrieve"]:
            return queryset.prefetch_related("facilities")
        return queryset


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
