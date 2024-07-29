import django_filters


from .models import City, \
                    Continent, \
                    Country, \
                    Currency, \
                    Language, \
                    Region


class CityFilter(django_filters.FilterSet):
    class Meta:
        model = City
        exclude = ['geo']


class ContinentFilter(django_filters.FilterSet):
    class Meta:
        model = Continent
        fields = {
            "name": ("iexact", "icontains", ),
            "iso_code": ("iexact", )
        }


class CountryFilter(django_filters.FilterSet):
    class Meta:
        model = Country
        fields = {
            "name": ("iexact", "icontains", ),
            "iso_code_2": ("iexact", ),
            "iso_code_3": ("iexact", ),
        }


# class CurrencyFilter(django_filters.FilterSet):
#     class Meta:
#         model = Currency


# class LanguageFilter(django_filters.FilterSet):
#     class Meta:
#         model = Language


class RegionFilter(django_filters.FilterSet):
    class Meta:
        model = Region
        fields = {
            "name": ("iexact", "icontains", ),
            "iso_code": ("iexact", ),
            "country__iso_code_2": ("iexact", )
        }
