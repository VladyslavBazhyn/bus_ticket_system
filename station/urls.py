from django.urls import path
from station.views import bus_list, bus_detail

app_name = "station"

urlpatterns = [
    path("buses/", bus_list, name="bus_list"),
    path("buses/<int:pk>/", bus_detail, name="bus_detail")
]

