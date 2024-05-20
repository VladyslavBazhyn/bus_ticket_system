from rest_framework import viewsets, mixins

from station.models import Buss
from station.serializers import BussSerializer


class BusViewSet(viewsets.ModelViewSet):
    queryset = Buss.objects.all()
    serializer_class = BussSerializer
