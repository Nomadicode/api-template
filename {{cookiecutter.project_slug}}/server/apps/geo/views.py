from rest_framework import viewsets

from utils.mixins.views import NestedParentViewMixin

from apps.geo.models import City, \
							Continent, \
							Country, \
							Currency, \
							Language, \
							Region
from apps.geo.serializers import CitySerializer, \
								 ContinentSerializer, \
								 CountrySerializer, \
								 CurrencySerializer, \
								 LanguageSerializer, \
								 RegionSerializer
from apps.geo.filters import CityFilter, \
							 ContinentFilter, \
							 CountryFilter, \
							 RegionFilter


class ContinentViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Continent.objects.all()
	serializer_class = ContinentSerializer
	lookup_field = "iso_code__iexact"
	filterset_fields = ["name", "iso_code"]


class CountryViewSet(NestedParentViewMixin, viewsets.ReadOnlyModelViewSet):
	queryset = Country.objects.all()
	serializer_class = CountrySerializer
	lookup_field = "iso_code_2__iexact"
	parent_lookups = {
		"continent_iso_code__iexact": ("continent", "iso_code", "iexact", ), # object, field, optional specifiers (i.e. iexact, icontains)
	}


class RegionViewSet(NestedParentViewMixin, viewsets.ReadOnlyModelViewSet):
	queryset = Region.objects.all()
	serializer_class = RegionSerializer
	lookup_field = "iso_code__iexact"
	parent_lookups = {
		"country_iso_code_2__iexact": ("country", "iso_code_2", "iexact", )
	}
	


class CityViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = City.objects.all()
	serializer_class = CitySerializer
	parent_lookups = {
		"country_iso_code_2__iexact": ("country", "iso_code_2", "iexact", ),
		"region_iso_code__iexact": ("region", "iso_code", "iexact", )
	}


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Currency.objects.all()
	serializer_class = CurrencySerializer
	lookup_field = "iso_code__iexact"


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Language.objects.all()
	serializer_class = LanguageSerializer
	lookup_field = "alpha_2_code__iexact"
