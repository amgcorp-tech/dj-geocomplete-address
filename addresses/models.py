import logging
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


from addresses.managers import AvailableCountries, AvailableStates, AvailableRegions

User = get_user_model()


try:
    from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
except ImportError:
    from django.db.models.fields.related import (
        ReverseSingleRelatedObjectDescriptor as ForwardManyToOneDescriptor,
    )

logger = logging.getLogger(__name__)


__all__ = ["Region", "Country", "State", "Locality", "Address", "AddressField"]


class InconsistentDictError(Exception):
    pass


def _to_python(value):
    raw = value.get("raw", "")
    country = value.get("country", "")
    country_code = value.get("country_code", "")
    state = value.get("state", "")
    state_code = value.get("state_code", "")
    locality = value.get("locality", "")
    sublocality = value.get("sublocality", "")
    postal_town = value.get("postal_town", "")
    postal_code = value.get("postal_code", "")
    street_number = value.get("street_number", "")
    route = value.get("route", "")
    formatted = value.get("formatted", "")
    latitude = value.get("latitude", None)
    longitude = value.get("longitude", None)
    url = value.get("url", "")

    # If there is no value (empty raw) then return None.
    if not raw:
        return None

    # Fix issue with NYC boroughs (https://code.google.com/p/gmaps-api-issues/issues/detail?id=635)
    if not locality and sublocality:
        locality = sublocality

    # Fix issue with UK addresses with no locality
    # (https://github.com/furious-luke/django-address/issues/114)
    if not locality and postal_town:
        locality = postal_town

    # If we have an inconsistent set of value bail out now.
    if (country or state or locality) and not (country and state and locality):
        raise InconsistentDictError

    # Handle the country.
    try:
        country_obj = Country.objects.get(name=country, code=country_code)
    except Country.DoesNotExist:
        if country:
            if len(country_code) > Country._meta.get_field("code").max_length:
                if country_code != country:
                    raise ValueError(_("Invalid country code (too long): %s" % country_code))
                country_code = ""
            country_obj = Country.objects.create(name=country, code=country_code)
        else:
            country_obj = None

    # Handle the state.
    try:
        state_obj = State.objects.get(name=state, country=country_obj)
    except State.DoesNotExist:
        if state:
            if len(state_code) > State._meta.get_field("code").max_length:
                if state_code != state:
                    raise ValueError(_("Invalid state code (too long): %s" % state_code))
                state_code = ""
            state_obj = State.objects.create(name=state, code=state_code, country=country_obj)
        else:
            state_obj = None

    # Handle the locality.
    try:
        locality_obj = Locality.objects.get(name=locality, postal_code=postal_code, state=state_obj)
    except Locality.DoesNotExist:
        if locality:
            locality_obj = Locality.objects.create(name=locality, postal_code=postal_code, state=state_obj)
        else:
            locality_obj = None

    # Handle the address.
    try:
        if not (street_number or route or locality):
            address_obj = Address.objects.get(raw=raw)
        else:
            address_obj = Address.objects.get(street_number=street_number, route=route, locality=locality_obj)
    except Address.DoesNotExist:
        address_obj = Address(
            street_number=street_number,
            route=route,
            raw=raw,
            locality=locality_obj,
            formatted=formatted,
            latitude=latitude,
            longitude=longitude,
            gmap_url=url,
        )

        # If "formatted" is empty try to construct it from other values.
        if not address_obj.formatted:
            address_obj.formatted = str(address_obj)

        # Need to save.
        address_obj.save()

    # Done.
    return address_obj


##
# Convert a dictionary to an address.
##


def to_python(value):

    # Keep `None`s.
    if value is None:
        return None

    # Is it already an address object?
    if isinstance(value, Address):
        return value

    # If we have an integer, assume it is a model primary key.
    elif isinstance(value, int):
        return value

    # A string is considered a raw value.
    elif isinstance(value, str):
        obj = Address(raw=value)
        obj.save()
        return obj

    # A dictionary of named address components.
    elif isinstance(value, dict):

        # Attempt a conversion.
        try:
            return _to_python(value)
        except InconsistentDictError:
            return Address.objects.create(raw=value["raw"])

    # Not in any of the formats I recognise.
    raise ValidationError(_("Invalid address value."))


class Country(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name=_("Country Name"))
    code = models.CharField(max_length=2, db_index=True, unique=True)
    code3 = models.CharField(max_length=3, db_index=True, unique=True, null=True, blank=True)
    phone_code = models.CharField(max_length=20, blank=True)
    capital = models.CharField(max_length=200, blank=True)
    currency = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True, help_text=_("Use as valid Country"))

    history = HistoricalRecords(
        history_id_field=models.UUIDField(default=uuid.uuid4)
    )

    objects = models.Manager()
    available_objects = AvailableCountries()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("countries_edit", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse_lazy("countries_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        """
        Ajax delete action is handled by Country API
        :return:
        """
        return reverse_lazy("country-detail", kwargs={"pk": self.pk})

    def country_short(self):
        return self.code

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ["name", "code"]


class Region(models.Model):
    name = models.CharField(verbose_name=_("Region Name"), max_length=50, unique=True)
    countries = models.ManyToManyField(Country, blank=True, related_name="regions")
    active = models.BooleanField(verbose_name=_("Active"), default=True)

    history = HistoricalRecords(
        history_id_field=models.UUIDField(default=uuid.uuid4)
    )

    objects = models.Manager()
    available_objects = AvailableRegions()

    def __str__(self):
        return self.name

    @property
    def total_countries(self):
        return self.countries.count()

    def get_absolute_url(self):
        return reverse_lazy("regions_edit", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse_lazy("regions_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        """
        Ajax delete action is handled by State API
        :return:
        """
        return reverse_lazy("region-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ("name",)


class State(models.Model):
    name = models.CharField(max_length=165, blank=True)
    code = models.CharField(max_length=8, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")
    is_active = models.BooleanField(verbose_name=_("Active"), default=True, help_text=_("Make a Valid State"))

    history = HistoricalRecords(
        history_id_field=models.UUIDField(default=uuid.uuid4)
    )

    objects = models.Manager()
    available_objects = AvailableStates()

    def get_absolute_url(self):
        return reverse_lazy("states_edit", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse_lazy("states_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        """
        Ajax delete action is handled by State API
        :return:
        """
        return reverse_lazy("state-detail", kwargs={"pk": self.pk})

    def abbr(self):
        if self.code:
            return self.code
        else:
            return self.name

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")
        unique_together = ("name", "country")
        ordering = ("country", "name")

    def __str__(self):
        txt = self.to_str()
        country = "%s" % self.country
        if country and txt:
            txt += ", "
        txt += country
        return txt

    def to_str(self):
        return "%s" % (self.name or self.code)


class Locality(models.Model):
    name = models.CharField(max_length=165, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="localities")

    history = HistoricalRecords(
        history_id_field=models.UUIDField(default=uuid.uuid4)
    )

    class Meta:
        verbose_name = _("Locality")
        verbose_name_plural = _("Localities")
        unique_together = ("name", "postal_code", "state")
        ordering = ("state", "name")

    def __str__(self):
        txt = "%s" % self.name
        state = self.state.to_str() if self.state else ""
        if txt and state:
            txt += ", "
        txt += state
        if self.postal_code:
            txt += " %s" % self.postal_code
        cntry = "%s" % (self.state.country if self.state and self.state.country else "")
        if cntry:
            txt += ", %s" % cntry
        return txt


##
# An address. If for any reason we are unable to find a matching
# decomposed address we will store the raw address string in `raw`.
##


class Address(models.Model):
    street_number = models.CharField(max_length=20, blank=True)
    route = models.CharField(max_length=100, blank=True)
    locality = models.ForeignKey(
        Locality,
        on_delete=models.CASCADE,
        related_name="addresses",
        blank=True,
        null=True,
    )
    raw = models.CharField(max_length=200)
    formatted = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    gmap_url = models.URLField(verbose_name=_("Url"), max_length=250, null=True, blank=True)
    waze_url = models.URLField(verbose_name=_("Waze Url"), max_length=250, null=True, blank=True)

    history = HistoricalRecords(
        history_id_field=models.UUIDField(default=uuid.uuid4)
    )

    def get_absolute_url(self):
        return reverse_lazy("address_edit", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse_lazy("address_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        """
        Ajax delete action is handled by State API
        :return:
        """
        return reverse_lazy("address-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        ordering = ("locality", "route", "street_number")

    def __str__(self):
        if self.formatted != "":
            txt = "%s" % self.formatted
        elif self.locality:
            txt = ""
            if self.street_number:
                txt = "%s" % self.street_number
            if self.route:
                if txt:
                    txt += " %s" % self.route
            locality = "%s" % self.locality
            if txt and locality:
                txt += ", "
            txt += locality
        else:
            txt = "%s" % self.raw
        return txt

    def clean(self):
        if not self.raw:
            raise ValidationError(_("Addresses may not have a blank `raw` field."))

    def as_dict(self):
        ad = dict(
            street_number=self.street_number,
            route=self.route,
            raw=self.raw,
            formatted=self.formatted,
            latitude=self.latitude if self.latitude else "",
            longitude=self.longitude if self.longitude else "",
        )
        if self.locality:
            ad["locality"] = self.locality.name
            ad["postal_code"] = self.locality.postal_code
            if self.locality.state:
                ad["state"] = self.locality.state.name
                ad["state_code"] = self.locality.state.code
                if self.locality.state.country:
                    ad["country"] = self.locality.state.country.name
                    ad["country_code"] = self.locality.state.country.code
        return ad


class AddressDescriptor(ForwardManyToOneDescriptor):
    def __set__(self, inst, value):
        super(AddressDescriptor, self).__set__(inst, to_python(value))


##
# A field for addresses in other models.
##


class AddressField(models.ForeignKey):
    description = _("An address")

    def __init__(self, *args, **kwargs):
        kwargs["to"] = "addresses.Address"
        # The address should be set to null when deleted if the relationship could be null
        default_on_delete = models.SET_NULL if kwargs.get("null", False) else models.CASCADE
        kwargs["on_delete"] = kwargs.get("on_delete", default_on_delete)
        super(AddressField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        from addresses.compat import compat_contribute_to_class

        compat_contribute_to_class(self, cls, name, virtual_only)

        setattr(cls, self.name, AddressDescriptor(self))

    def formfield(self, **kwargs):
        from .forms import AddressField as AddressFormField

        defaults = dict(form_class=AddressFormField)
        defaults.update(kwargs)
        return super(AddressField, self).formfield(**defaults)