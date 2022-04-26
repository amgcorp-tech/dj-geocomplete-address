from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from addresses.models import State, Locality, Address, Country, Region


class UnidentifiedListFilter(SimpleListFilter):
    title = "unidentified"
    parameter_name = "unidentified"

    def lookups(self, request, model_admin):
        return (("unidentified", "unidentified"),)

    def queryset(self, request, queryset):
        if self.value() == "unidentified":
            return queryset.filter(locality=None)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active")
    list_editable = ("name", "active")
    search_fields = ("name",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "is_active")
    list_editable = ("name", "code", "is_active")
    search_fields = ("name", "code",)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    search_fields = ("name", "code")


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    search_fields = ("name", "postal_code")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = ("street_number", "route", "raw")
    list_filter = (UnidentifiedListFilter,)
