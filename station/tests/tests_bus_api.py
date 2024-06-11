from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Buss, Facility
from station.serializers import BussListSerializer, BussRetrieveSerializer

BUS_URL = reverse("station:buss-list")  # or bus??


def sample_bus(**params) -> Buss:
    default = {
        "info": "AA 0000 BB",
        "num_seats": 50
    }
    default.update(params)
    return Buss.objects.create(**default)


def detail_url(bus_id: int):  #127.0.0.1:8000/api/v1/station/buses/<bus_id>
    return reverse("station:buss-detail", args=(bus_id,))


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

    def test_retrieve_bus_detail(self):
        bus = sample_bus()
        bus.facilities.add(Facility.objects.create(name="Wifi"))

        url = detail_url(bus.id)

        res = self.client.get(url)

        serializer = BussRetrieveSerializer(bus)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)

    def test_create_buss_forbidden(self):
        payload = {
            "info": "AA 9999 BB",
            "num_seats": 60
        }
        res = self.client.post(BUS_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBussTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.test",
            password="adminpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_buss(self):
        payload = {
            "info": "AA 9999 BB",
            "num_seats": 60
        }
        res = self.client.post(BUS_URL, payload)

        bus = Buss.objects.get(id=res.data["id"])

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(bus, key))

    def test_create_buss_with_facilities(self):
        facility_1 = Facility.objects.create(name="Wifi")
        facility_2 = Facility.objects.create(name="WC")

        payload = {
            "info": "AA 9999 BB",
            "num_seats": 60,
            "facilities": [facility_1.id, facility_2.id]
        }

        res = self.client.post(BUS_URL, payload)

        bus = Buss.objects.get(id=res.data["id"])

        facilities = bus.facilities.all()

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(facility_1, facilities)
        self.assertIn(facility_2, facilities)
        self.assertEqual(facilities.count(), 2)

    def test_delete_buss_not_allowed(self):

        bus = sample_bus()

        url = detail_url(bus.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
