from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("regions", RegionsViewSet, basename="region")
router.register("countries", CountryViewSet, basename="country")
router.register("states", StateViewSet, basename="state")
router.register("address", AddressViewSet, basename="address")


urlpatterns = [
    path("", include(router.urls)),
]
