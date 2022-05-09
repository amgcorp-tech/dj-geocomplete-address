from django import forms
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .app_settings import discover_addresses_settings
from .models import Address


google_api_key = discover_addresses_settings()


class AddressWidget(forms.TextInput):
    components = [
        ("country", "country"),
        ("country_code", "country_short"),
        ("locality", "locality"),
        ("sublocality", "sublocality"),
        ("postal_code", "postal_code"),
        ("postal_town", "postal_town"),
        ("route", "route"),
        ("street_number", "street_number"),
        ("state", "administrative_area_level_1"),
        ("state_code", "administrative_area_level_1_short"),
        ("formatted", "formatted_address"),
        ("latitude", "lat"),
        ("longitude", "lng"),
        ("url", "url")
    ]

    class Media:
        """Media defined as a dynamic property instead of an inner class."""

        js = [
            "https://maps.googleapis.com/maps/api/js?libraries=places&key=%s&language=en" % google_api_key,
            "addresses/js/geocomplete/jquery.geocomplete.min.js",
            "addresses/address/js/address.js",
        ]

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get("attrs", {})
        classes = attrs.get("class", "")
        classes += (" " if classes else "") + "address"
        attrs["class"] = classes
        kwargs["attrs"] = attrs
        super(AddressWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):

        # Can accept None, a dictionary of values or an Address object.
        if value in (None, ""):
            ad = {}
        elif isinstance(value, dict):
            ad = value
        elif isinstance(value, int):
            ad = Address.objects.get(pk=value)
            ad = ad.as_dict()
        else:
            ad = value.as_dict()

        # Generate the elements. We should create a suite of hidden fields
        # For each individual component, and a visible field for the raw
        # input. Begin by generating the raw input.
        elems = [super(AddressWidget, self).render(name, escape(ad.get("formatted", "")), attrs, **kwargs)]

        # Now add the hidden fields.
        elems.append('<div id="%s_components" style="display: none;">' % name)
        for com in self.components:
            elems.append(
                '<input type="hidden" name="%s_%s" data-geo="%s" value="%s" />'
                % (name, com[0], com[1], escape(ad.get(com[0], "")))
            )
        elems.append("</div>")

        return mark_safe("\n".join(elems))

    def value_from_datadict(self, data, files, name):
        raw = data.get(name, "")
        if not raw:
            return raw
        ad = dict([(c[0], data.get(name + "_" + c[0], "")) for c in self.components])
        ad["raw"] = raw
        return ad
