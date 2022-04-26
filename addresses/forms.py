from django import forms
from django.utils.translation import gettext_lazy as _
from django_select2.forms import ModelSelect2Widget

from .models import Address, to_python, Country, State, Region, Locality

from .widgets import AddressWidget


__all__ = ["AddressWidget", "AddressField", "CountryForm", "StateForm", "RegionForm"]


class AddressField(forms.ModelChoiceField):
    widget = AddressWidget

    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Address.objects.none()
        super(AddressField, self).__init__(*args, **kwargs)

    def to_python(self, value):

        # Treat `None`s and empty strings as empty.
        if value is None or value == "":
            return None

        # Check for garbage in the lat/lng components.
        for field in ["latitude", "longitude"]:
            if field in value:
                if value[field]:
                    try:
                        value[field] = float(value[field])
                    except Exception:
                        raise forms.ValidationError(
                            "Invalid value for %(field)s",
                            code="invalid",
                            params={"field": field},
                        )
                else:
                    value[field] = None

        return to_python(value)


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ["name", "code", "code3", "phone_code", "currency", "is_active"]


class StateForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        label=u"Country",
        widget=ModelSelect2Widget(
            model=Country,
            search_fields=["name__icontains", "code__icontains", "code3__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta:
        model = State
        fields = ["country", "name", "code"]


class RegionForm(forms.ModelForm):
    countries = forms.ModelMultipleChoiceField(queryset=Country.objects.all(), required=False, label=_("Countries"))

    class Meta:
        model = Region
        fields = ["name", "countries", "active"]


class AddressForm(forms.ModelForm):
    locality = forms.ModelChoiceField(
        queryset=Locality.objects.all(),
        label=u"Locality",
        widget=ModelSelect2Widget(
            model=Locality,
            search_fields=["name__icontains", "postal_code__icontains",
                           "state__name__icontains", "state__code__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta:
        model = Address
        fields = ("raw", "formatted", "street_number", "route", "locality", "latitude", "longitude", "gmap_url", "waze_url")


class RegisterAddressForm(forms.Form):
    address = AddressField(label=_("Address"), required=True,)