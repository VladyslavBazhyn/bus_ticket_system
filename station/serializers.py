from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from station.models import Buss, Trip, Facility, Ticket, Order


class BussSerializer(serializers.ModelSerializer):
    # is_small = serializers.ReadOnlyField() # if fields = "__all__"
    class Meta:
        model = Buss
        fields = [
            "id",
            "info",
            "num_seats",
            "is_small",
            "facilities"
        ]
        read_only_fields = ["id"]
    # id = serializers.IntegerField(read_only=True)
    # info = serializers.CharField(required=False, max_length=255)
    # num_seats = serializers.IntegerField(required=True)
    #
    # def create(self, validated_data):
    #     return Buss.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.info = validated_data.get("info", instance.info)
    #     instance.num_seats = validated_data.get("num_seats", instance.num_seats)
    #     instance.save()
    #     return instance


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "seat",
            "trip"
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=["seat", "trip"]
            )
        ]

    def validate(self, attrs):
        Ticket.validate_seat(
            attrs["seat"],
            attrs["trip"].bus.num_seats,
            serializers.ValidationError
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "tickets"
        ]

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            "id",
            "source",
            "destination",
            "departure",
            "bus",
        ]


class TripListSerializer(serializers.ModelSerializer):
    bus_info = serializers.CharField(source="bus.info", read_only=True)
    bus_num_seats = serializers.IntegerField(source="bus.num_seats", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "source",
            "destination",
            "departure",
            "bus_info",
            "bus_num_seats",
            "tickets_available"
        ]


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = [
            "id",
            "name"
        ]


class BussRetrieveSerializer(BussSerializer):
    facilities = FacilitySerializer(many=True)


class TripRetrieveSerializer(TripSerializer):
    bus = BussRetrieveSerializer(many=False, read_only=True)
    taken_seats = serializers.SlugRelatedField(
        slug_field="seat",
        many=True,
        read_only=True,
        source="tickets"
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "source",
            "destination",
            "departure",
            "bus",
            "taken_seats"
        ]


class TicketListSerializer(TicketSerializer):
    trip = TripListSerializer(read_only=True)


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(read_only=True, many=True)


class BussListSerializer(BussSerializer):
    facilities = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
