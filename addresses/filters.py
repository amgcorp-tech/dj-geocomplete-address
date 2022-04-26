import django_filters
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet
from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import Country, State, Region, Address, Locality

CHOICES_BOOLEAN_FILTER = (
    (0, _('NO')),
    (1, _('YES')),
)


class SearchFilter(FilterSet):
    search = django_filters.CharFilter(label=_("Search"), method="my_custom_filter")

    class Meta:
        fields = ("search",)

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })


class CountryFilter(SearchFilter):
    search = django_filters.CharFilter(label=_("Search"), method="my_custom_filter")
    is_active = django_filters.ChoiceFilter(field_name="is_active", label=_('Active'),
                                            choices=CHOICES_BOOLEAN_FILTER, widget=Select2Widget())

    class Meta:
        model = Country
        fields = ("search", "is_active",)

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value) | queryset.filter(code__icontains=value) | \
               queryset.filter(code3__icontains=value) | queryset.filter(currency__icontains=value)


class StateFilter(SearchFilter):
    search = django_filters.CharFilter(label=_("Search"), method="my_custom_filter")
    is_active = django_filters.ChoiceFilter(field_name="is_active", label=_('Active'),
                                            choices=CHOICES_BOOLEAN_FILTER, widget=Select2Widget())
    country = django_filters.ModelChoiceFilter(
        queryset=Country.objects.filter(is_active=True),
        label=u"Country",
        required=False,
        widget=ModelSelect2Widget(
            model=Country,
            search_fields=["name__icontains", "code__icontains"],
            max_results=500,
            attrs={
                'data-minimum-input-length': 0
            },
        ),
    )

    class Meta:
        model = State
        fields = ("search", "is_active")

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value) | queryset.filter(code__icontains=value)


class RegionsFilter(SearchFilter):
    search = django_filters.CharFilter(label=_("Search"), method="my_custom_filter")
    active = django_filters.ChoiceFilter(field_name="active", label=_('Active'),
                                         choices=CHOICES_BOOLEAN_FILTER, widget=Select2Widget())

    class Meta:
        model = Region
        fields = ("search", "active",)

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class AddressFilter(SearchFilter):
    search = django_filters.CharFilter(label=_("Search"), method="my_custom_filter")
    locality = django_filters.ModelChoiceFilter(
        queryset=Locality.objects.all(),
        label=u"Locality",
        required=False,
        widget=ModelSelect2Widget(
            model=Locality,
            search_fields=["name__icontains", "postal_code__icontains",
                           "state__name__icontains", "state__code__icontains"],
            max_results=500,
            attrs={
                'data-minimum-input-length': 0
            },
        ),
    )

    class Meta:
        model = Address
        fields = ("search", "locality",)

    def my_custom_filter(self, queryset, name, value):
        return (
            queryset.filter(raw__icontains=value) |
            queryset.filter(formatted__icontains=value) |
            queryset.filter(route__icontains=value) |
            queryset.filter(street_number__icontains=value) |
            queryset.filter(locality__name__icontains=value) |
            queryset.filter(locality__postal_code__icontains=value) |
            queryset.filter(locality__state__name__icontains=value) |
            queryset.filter(locality__state__code__icontains=value)
        )