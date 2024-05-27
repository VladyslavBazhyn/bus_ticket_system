from rest_framework import serializers

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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "user",
            "tickets"
        ]


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            "id",
            "source",
            "destination",
            "departure",
            "bus"
        ]


class TripListSerializer(serializers.ModelSerializer):

    bus_info = serializers.CharField(source=Buss.info, read_only=True)
    bus_num_seats = serializers.IntegerField(source=Buss.num_seats, read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "source",
            "destination",
            "departure",
            "bus_info",
            "bus_num_seats"
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


class BussListSerializer(BussSerializer):
    facilities = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
