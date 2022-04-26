from django.db import models


class AvailableRegions(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class AvailableCountries(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AvailableStates(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, country__is_active=True)