from rest_framework import serializers

from apps.geo.models import City, \
                            Continent, \
                            Country, \
                            Currency, \
                            Language, \
                            Region


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"
        lookup_field = "iso_code"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"
        lookup_field = "alpha_2_code"


class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = "__all__"
        lookup_field = "iso_code"


class CountrySerializer(serializers.ModelSerializer):
    continent = ContinentSerializer()
    currency = CurrencySerializer()
    languages = LanguageSerializer(many=True)

    class Meta:
        model = Country
        fields = "__all__"
        lookup_field = "iso_code_2"


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Region
        fields = "__all__"
    

class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    country = CountrySerializer()

    class Meta:
        model = City
        fields = "__all__"
