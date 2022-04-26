from rest_framework import serializers, exceptions

from ..forms import AddressField
from ..models import Country, State, Address, Region, Locality


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "code",
        )


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_active=True)
        return super().to_representation(data)


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = State
        fields = (
            "id",
            "name",
            "code",
            "country",
        )


# Serializer for the model Country
class CountryListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "code",
            "code3",
            "phone_code",
            "currency",
        )


class CountryDetailSerializer(serializers.HyperlinkedModelSerializer):
    states = StateSerializer(many=True)

    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "code",
            "code3",
            "phone_code",
            "currency",
            "states",
        )
        depth = 1


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = (
            "id",
            "name",
        )


class RegionDetailSerializer(serializers.ModelSerializer):
    countries = CountryListSerializer(many=True)

    class Meta:
        model = Region
        fields = (
            "id",
            "name",
            "countries",
        )


class LocalitySerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = Locality
        fields = (
            "id",
            "name",
            "postal_code",
            "state"
        )


class AddressSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer(read_only=True)

    class Meta:
        model = Address
        fields = (
            'id',
            'raw',
            'street_number',
            'route',
            'locality',
            'formatted',
            'latitude',
            'longitude',
            'gmap_url',
            'waze_url',
        )


class CreateAddressSerializer(serializers.ModelSerializer):
    raw = AddressField()

    class Meta:
        model = Address
        fields = ('raw',)