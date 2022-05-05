"""URLs for the addresses app."""
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.MainTemplateView.as_view(), name='addresses_main'),

    path("countries/", views.ManageCountryView.as_view(), name="countries_manage"),
    path("countries/new/", views.CountryCreateView.as_view(), name="countries_new"),
    path("countries/<pk>/edit", views.CountryUpdateView.as_view(), name="countries_edit"),
    path("countries/bulk/remove/", views.BulkDeleteCountryView.as_view(), name="countries_delete_bulk"),
    path("countries/bulk/activate/", views.BulkActivateCountryView.as_view(), name="countries_activate_bulk"),
    path("countries/bulk/activate-all/", views.BulkActivateAllCountryView.as_view(), name="countries_activate_all_bulk"),
    path("countries/bulk/deactivate/", views.BulkDeactivateCountryView.as_view(), name="countries_deactivate_bulk"),
    path("countries/bulk/deactivate-all/", views.BulkDeactivateAllCountryView.as_view(),
         name="countries_deactivate_all_bulk"),


    path("states/", views.ManageStateView.as_view(), name="states_manage"),
    path("states/new/", views.StateCreateView.as_view(), name="states_new"),
    path("states/<pk>/edit", views.StateUpdateView.as_view(), name="states_edit"),
    path("states/bulk/remove/", views.BulkDeleteStateView.as_view(), name="states_delete_bulk"),
    path("states/bulk/activate/", views.BulkActivateStateView.as_view(), name="states_activate_bulk"),
    path("states/bulk/activate-all/", views.BulkActivateAllStateView.as_view(), name="states_activate_all_bulk"),
    path("states/bulk/deactivate/", views.BulkDeactivateStateView.as_view(), name="states_deactivate_bulk"),
    path("states/bulk/deactivate-all/", views.BulkDeactivateAllStateView.as_view(), name="states_deactivate_all_bulk"),


    path("regions/", views.ManageRegionsView.as_view(), name="regions_manage"),
    path("regions/new/", views.RegionCreateView.as_view(), name="regions_new"),
    path("regions/<pk>/edit", views.RegionUpdateView.as_view(), name="regions_edit"),
    path("regions/bulk/remove/", views.BulkDeleteRegionsView.as_view(), name="regions_delete_bulk"),


    path("address/", views.ManageAddressView.as_view(), name="address_manage"),
    path("address/new/", views.AddressCreateView.as_view(), name="address_new"),
    path("address/<pk>/edit", views.AddressUpdateView.as_view(), name="address_edit"),
    path("address/bulk/remove/", views.BulkDeleteAddressView.as_view(), name="address_delete_bulk"),

]
