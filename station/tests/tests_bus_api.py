from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Buss, Facility
from station.serializers import BussListSerializer

BUS_URL = reverse("station:buss-list")  # or bus??


def sample_bus(**params) -> Buss:
    default = {
        "info": "AA 0000 BB",
        "num_seats": 50
    }
    default.update(params)
    return Buss.objects.create(**default)


class UnauthenticatedBusApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BUS_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBusApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_buses_list(self):
        sample_bus()
        bus_with_facilities = sample_bus()

        facility_1 = Facility.objects.create(name="Wifi")
        facility_2 = Facility.objects.create(name="WC")

        bus_with_facilities.facilities.add(facility_1, facility_2)

        res = self.client.get(BUS_URL)
        busses = Buss.objects.all()
        serializer = BussListSerializer(busses, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)  # ??? IN wideo I have res.data["results"] and serializer.data

    def test_filter_busses_by_facilities(self):
        bus_without_facility = sample_bus()
        bus_with_facility_1 = sample_bus(info="AA 0001 BB")
        bus_with_facility_2 = sample_bus(info="AA 0002 BB")

        facility_1 = Facility.objects.create(name="Wifi")
        facility_2 = Facility.objects.create(name="WC")

        bus_with_facility_1.facilities.add(facility_1)
        bus_with_facility_2.facilities.add(facility_2)

        res = self.client.get(
            BUS_URL,
            {
                "facilities": f"{facility_1.id},{facility_2.id}"
            }
        )

        serializer_without_facility = BussListSerializer(bus_without_facility)
        serializer_bus_facility_1 = BussListSerializer(bus_with_facility_1)
        serializer_bus_facility_2 = BussListSerializer(bus_with_facility_2)

        self.assertIn(serializer_bus_facility_1.data, res.data)
        self.assertIn(serializer_bus_facility_2.data, res.data)
        self.assertNotIn(serializer_without_facility.data, res.data)
