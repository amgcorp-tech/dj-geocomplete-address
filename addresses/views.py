"""Views for the addresses app."""
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, FormView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.export import ExportMixin

from addresses.filters import CountryFilter, StateFilter, RegionsFilter, AddressFilter
from addresses.forms import CountryForm, StateForm, RegionForm, AddressForm, RegisterAddressForm
from addresses.models import Country, State, Region, Address
from addresses.tables import CountryTable, StateTable, RegionsTable, AddressTable


class MainTemplateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    """Main template view. Remove it if you don't need it."""
    permission_required = "addresses.view_address"
    template_name = "addresses/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Django Addresses")

        return context


class ManageCountryView(PermissionRequiredMixin, LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = "addresses.view_country"
    table_class = CountryTable
    exclude_columns = ("selection", "actions")
    model = Country
    filterset_class = CountryFilter
    paginate_by = 50
    strict = False
    template_name = "addresses/countries/manage.html"

    def get_context_data(self, **kwargs):
        context = super(ManageCountryView, self).get_context_data(**kwargs)
        context["title"] = _("Countries")

        return context


class CountryCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "addresses.add_country"
    model = Country
    form_class = CountryForm
    template_name = "addresses/countries/form.html"

    def form_valid(self, form):
        country = form.save()
        messages.success(self.request, _("New Country registered: " + country.name.upper()))
        return redirect(reverse_lazy("countries_manage"))

    def get_context_data(self, **kwargs):
        context = super(CountryCreateView, self).get_context_data(**kwargs)
        context["title"] = _("New Country")

        return context


class CountryUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "addresses.change_country"
    model = Country
    form_class = CountryForm
    template_name = "addresses/countries/form.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Country updated!"))
        return redirect(reverse_lazy("countries_manage"))

    def get_context_data(self, **kwargs):
        context = super(CountryUpdateView, self).get_context_data(**kwargs)
        context["title"] = _("Edit Country")

        return context


class BulkDeleteCountryView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.delete_country"

    def post(self, *args, **kwargs):
        selection = self.request.POST.getlist("selection[]")

        if len(selection) > 0:

            objects = Country.objects.filter(pk__in=selection)
            objects.delete()
            messages.success(self.request, _("Country deleted successfully"))

        else:
            messages.info(self.request, _("No Countries selected"))
        return redirect(reverse_lazy("countries_manage"))


class BulkActivateCountryView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.change_country"

    def post(self, *args, **kwargs):
        selection = self.request.POST.getlist("selection[]")

        if len(selection) > 0:

            objects = Country.objects.filter(pk__in=selection).update(is_active=True)
            messages.success(self.request, _(f"{objects} Countries activated"))

        else:
            messages.info(self.request, _("No Countries selected"))
        return redirect(reverse_lazy("countries_manage"))


class BulkActivateAllCountryView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.change_country"

    def post(self, *args, **kwargs):
        objects = Country.objects.filter(is_active=False).update(is_active=True)
        messages.success(self.request, _(f"{objects} Countries activated"))

        return redirect(reverse_lazy("countries_manage"))


class BulkDeactivateCountryView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.change_country"

    def post(self, *args, **kwargs):
        selection = self.request.POST.getlist("selection[]")

        if len(selection) > 0:

            objects = Country.objects.filter(pk__in=selection).update(is_active=False)
            messages.success(self.request, _(f"{objects} Countries deactivated"))

        else:
            messages.info(self.request, _("No Countries selected"))
        return redirect(reverse_lazy("countries_manage"))


class BulkDeactivateAllCountryView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.change_country"

    def post(self, *args, **kwargs):
        objects = Country.objects.filter(is_active=True).update(is_active=False)
        messages.success(self.request, _(f"{objects} Countries deactivated"))

        return redirect(reverse_lazy("countries_manage"))


class ManageStateView(PermissionRequiredMixin, LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = "addresses.view_state"
    table_class = StateTable
    exclude_columns = ("selection", "actions")
    model = State
    filterset_class = StateFilter
    paginate_by = 50
    strict = False
    template_name = "addresses/states/manage.html"

    def get_context_data(self, **kwargs):
        context = super(ManageStateView, self).get_context_data(**kwargs)
        context["title"] = _("States")

        return context


class StateCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "addresses.add_state"
    model = State
    form_class = StateForm
    template_name = "addresses/states/form.html"

    def form_valid(self, form):
        state = form.save()
        messages.success(self.request, _("New State registered: " + state.name_std.upper()))
        return redirect(reverse_lazy("states_manage"))

    def get_context_data(self, **kwargs):
        context = super(StateCreateView, self).get_context_data(**kwargs)
        context["title"] = _("New State")

        return context


class StateUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "addresses.change_state"
    model = State
    form_class = StateForm
    template_name = "addresses/states/form.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("State updated!"))
        return redirect(reverse_lazy("states_manage"))

    def get_context_data(self, **kwargs):
        context = super(StateUpdateView, self).get_context_data(**kwargs)
        context["title"] = _("Edit State")

        return context


class BulkDeleteStateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.delete_state"

    def post(self, *args, **kwargs):
        selection = self.request.POST.getlist("selection[]")

        if len(selection) > 0:

            objects = State.objects.filter(pk__in=selection)
            objects.delete()
            messages.success(self.request, _("States deleted successfully"))

        else:
            messages.info(self.request, _("No States selected"))
        return redirect(reverse_lazy("states_manage"))


class BulkActivateStateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.change_state"

    def post(self, *args, **kwargs):
        selection = self.request.POST.getlist("selection[]")

        if len(selection) > 0:

            objects = State.objects.filter(pk__in=selection).update(is_active=True)
            messages.success(self.request, _(f"{objects} States activated"))

        else:
            messages.info(self.request, _("No States selected"))
        return redirect(reverse_lazy("states_manage"))


class BulkActivateAllStateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.change_state"

    def post(self, *args, **kwargs):
        objects = State.objects.filter(is_active=False).update(is_active=True)
        messages.success(self.request, _(f"{objects} States activated"))

        return redirect(reverse_lazy("states_manage"))


class BulkDeactivateStateView(LoginRequiredMixin, View):
    permission_required = "addresses.change_state"

    def post(self, *args, **kwargs):
        selection = self.request.POST.getlist("selection[]")

        if len(selection) > 0:

            objects = State.objects.filter(pk__in=selection).update(is_active=False)
            messages.success(self.request, _(f"{objects} States deactivated"))

        else:
            messages.info(self.request, _("No States selected"))
        return redirect(reverse_lazy("states_manage"))


class BulkDeactivateAllStateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.change_state"

    def post(self, *args, **kwargs):
        objects = State.objects.filter(is_active=True).update(is_active=False)
        messages.success(self.request, _(f"{objects} States deactivated"))

        return redirect(reverse_lazy("states_manage"))


class ManageRegionsView(PermissionRequiredMixin, LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = "addresses.view_region"
    table_class = RegionsTable
    exclude_columns = ("selection", "actions")
    model = Region
    filterset_class = RegionsFilter
    paginate_by = 50
    strict = False
    template_name = "addresses/regions/manage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Regions")

        return context


class RegionCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "addresses.add_region"
    model = Region
    form_class = RegionForm
    template_name = "addresses/regions/form.html"

    def form_valid(self, form):
        region = form.save()
        messages.success(self.request, _("New Region registered: " + region.name.upper()))
        return redirect(reverse_lazy("regions_manage"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("New Region")

        return context


class RegionUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "addresses.change_region"
    model = Region
    form_class = RegionForm
    template_name = "addresses/regions/form.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Region updated!"))
        return redirect(reverse_lazy("regions_manage"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Region")

        return context


class BulkDeleteRegionsView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.delete_region"

    def post(self, *args, **kwargs):
        selection = self.request.POST.getlist("selection[]")

        if len(selection) > 0:

            objects = Region.objects.filter(pk__in=selection)
            objects.delete()
            messages.success(self.request, _("Regions deleted successfully"))

        else:
            messages.info(self.request, _("No Regions selected"))
        return redirect(reverse_lazy("regions_manage"))


class ManageAddressView(PermissionRequiredMixin, LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = "addresses.view_address"
    table_class = AddressTable
    exclude_columns = ("selection", "actions")
    model = Address
    filterset_class = AddressFilter
    paginate_by = 50
    strict = False
    template_name = "addresses/address/manage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Address")

        return context


class AddressCreateView(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    permission_required = "addresses.add_address"
    form_class = RegisterAddressForm
    template_name = "addresses/address/form.html"

    def form_valid(self, form):
        instance = form.cleaned_data["address"]
        messages.success(self.request, _(f"New Address registered: {instance.formatted}"))
        return redirect(reverse_lazy("address_manage"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("New Address")

        return context


class AddressUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "addresses.change_address"
    model = Address
    form_class = AddressForm
    template_name = "addresses/address/form.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Address updated!"))
        return redirect(reverse_lazy("address_manage"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Address")

        return context


class BulkDeleteAddressView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "addresses.delete_address"

    def post(self, *args, **kwargs):
        selection = self.request.POST.getlist("selection[]")

        if len(selection) > 0:

            objects = Address.objects.filter(pk__in=selection)
            objects.delete()
            messages.success(self.request, _("Address deleted successfully"))

        else:
            messages.info(self.request, _("No Address selected"))
        return redirect(reverse_lazy("address_manage"))