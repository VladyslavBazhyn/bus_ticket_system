from django.db.models import Count, F
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from station.models import (
    Buss,
    Trip,
    Facility,
    Order
)
from station.serializers import (
    BussListSerializer,
    TripSerializer,
    TripListSerializer,
    BussSerializer,
    FacilitySerializer,
    BussRetrieveSerializer,
    TripRetrieveSerializer,
    OrderSerializer,
    OrderListSerializer,
    BussImageSerializer
)


# AllowANy - None
# IsAuthenticated - "list", "retrieve" (GET)
# IsAdminUser - "create", "update", "partial_update", "destroy" (POST, PUT, PATCH, DELETE)

class BusViewSet(viewsets.ModelViewSet):
    queryset = Buss.objects.all()
    serializer_class = BussSerializer

    @staticmethod
    def _param_to_ints(query_string):
        """Convert a string of format '1,2,3' to a list of integers [1, 2, 3]"""
        return [int(str_id) for str_id in query_string.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return BussListSerializer
        elif self.action == "retrieve":
            return BussRetrieveSerializer
        elif self.action == "upload_image":
            return BussImageSerializer

        return BussSerializer

    def get_queryset(self):
        queryset = self.queryset
        facilities = self.request.query_params.get("facilities")
        if facilities:
            facilities = self._param_to_ints(facilities)
            queryset = queryset.filter(facilities__id__in=facilities)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("facilities")

        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        bus = self.get_object()
        serializer = self.get_serializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "facilities",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by facility id (ex. ?facilities=2,3)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of busses"""
        return super().list(request, *args, **kwargs)


class OrderSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 20


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user.id)
        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__trip__bus")

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = OrderListSerializer

        return serializer_class

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
        if self.action == "retrieve":
            return queryset.select_related()
        elif self.action == "list":
            return (
                queryset
                .select_related()
                .annotate(tickets_available=F("bus__num_seats") - Count("tickets"))
            )
        return self.queryset.order_by("id")


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
