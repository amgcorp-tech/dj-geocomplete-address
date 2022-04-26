from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status, viewsets, exceptions
from django_filters import rest_framework as filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from ..api.serializers import (
    RegionSerializer,
    RegionDetailSerializer,
    CountryListSerializer,
    CountryDetailSerializer,
    StateSerializer,
    AddressSerializer,
    CreateAddressSerializer
)
from ..models import Region, Country, State, Address


class RegionsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegionSerializer

    def get_queryset(self):
        return Region.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RegionSerializer
        else:
            return RegionDetailSerializer

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Region, pk=kwargs["pk"])
        if request.user.has_perm("addresses.delete_region"):
            instance.delete()
            return Response(
                {
                    "error": False,
                    "message": _("Region deleted successfully!")
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": True,
                "message": _("Sorry, your user does not have permissions to perform this action")
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class CountryFilter(filters.FilterSet):
    code = filters.CharFilter(field_name="code", lookup_expr="iexact")

    class Meta:
        model = Country
        fields = ["code"]


class CountryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CountryFilter
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Country.available_objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CountryListSerializer
        if self.action == "retrieve":
            return CountryDetailSerializer

    @action(detail=False)
    def validate(self, request, pk=None):
        """
        Returns true if country exist and is active
        """
        country = Country.objects.filter(code__iexact=request.GET.get("country"))
        if country:
            return Response(
                data={"valid": True, "country": country.first().id},
                status=status.HTTP_200_OK,
            )
        return Response(data={"valid": False}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Country, pk=kwargs["pk"])
        if request.user.has_perm("addresses.delete_country"):
            instance.delete()
            return Response(
                {
                    "error": False,
                    "message": _("Country deleted successfully!")
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": True,
                "message": _("Sorry, your user does not have permissions to perform this action")
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class StateFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="iexact")

    class Meta:
        model = State
        fields = ["name"]


class StateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = StateSerializer
    queryset = State.available_objects.all()
    permission_classes = (AllowAny,)
    filterset_class = StateFilter

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(State, pk=kwargs["pk"])
        if request.user.has_perm("addresses.delete_state"):
            instance.delete()
            return Response(
                {
                    "error": False,
                    "message": _("State / Province deleted successfully!")
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": True,
                "message": _("Sorry, your user does not have permissions to perform this action")
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class AddressViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = AddressSerializer
    # pagination_class = None

    def get_queryset(self):
        return Address.objects.all()

    def get_serializer_class(self):
        # if self.request.method in ['POST', 'PUT', 'PATCH']: #and self.action in ['create', 'update', 'partial_update']:
        #     return CreateAddressSerializer

        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "error": False,
                "message": _(f"Address retrieved successfully!"),
                "result": serializer.data
            })
        raise ValidationError(
            {"error": True, "message": u"Sorry, an error has occurred!"}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except:
            raise exceptions.ValidationError(
                {"error": True, "message": u"Sorry, an error has occurred registered the address"}
            )

        extra_data = {
            "error": False,
            "message": u"Your address has been successfully registered!",
        }
        return Response(extra_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Address, pk=kwargs["pk"])
        if request.user.has_perm("addresses.delete_address"):
            instance.delete()
            return Response(
                {
                    "error": False,
                    "message": _("Address deleted successfully!")
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": True,
                "message": _("Sorry, your user does not have permissions to perform this action")
            },
            status=status.HTTP_403_FORBIDDEN,
        )