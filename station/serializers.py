from rest_framework import serializers
from station.models import Buss, Ticket, Order


class BussSerializer(serializers.ModelSerializer):
    # is_small = serializers.ReadOnlyField() # if fields = "__all__"
    class Meta:
        model = Buss
        fields = [
            "id",
            "info",
            "num_seats",
            "is_small"
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
