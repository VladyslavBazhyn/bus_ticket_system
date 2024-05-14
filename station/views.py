from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from station.models import Buss
from station.serializers import BussSerializer


@api_view(["GET", "POST"])
def bus_list(request) -> Response:
    if request.method == "GET":
        buses = Buss.objects.all()
        serializer = BussSerializer(buses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = BussSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def bus_detail(request, pk) -> Response:
    bus = get_object_or_404(Buss, pk=pk)
    if request.method == "GET":
        serializer = BussSerializer(bus)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = BussSerializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        bus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
