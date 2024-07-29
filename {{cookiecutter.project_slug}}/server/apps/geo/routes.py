from django.urls import path, include
from apps.geo.views import CityViewSet, \
                           ContinentViewSet, \
                           CountryViewSet, \
                           CurrencyViewSet, \
                           LanguageViewSet, \
                           RegionViewSet

from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

APP_PREFIX = 'geo/'

router = SimpleRouter()
router.register(r'continents', ContinentViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'languages', LanguageViewSet)

continent_nested_router = NestedSimpleRouter(router, r'continents', lookup='continent')
continent_nested_router.register(r'countries', CountryViewSet)

country_nested_router = NestedSimpleRouter(router, r'countries', lookup='country')
country_nested_router.register(r'regions', RegionViewSet)
country_nested_router.register(r'cities', CityViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(continent_nested_router.urls)),
    path(r'', include(country_nested_router.urls)),
]


# urlpatterns = [
#     path('continents/', ContinentViewSet.as_view()),
#     path('continents/<slug:parent_code>/countries/', CountryViewSet.as_view({'get': 'list'})),
    
#     path('countries/', CountryViewSet),

#     path('countries/<slug:parent_code>/regions/', RegionViewSet.as_view({'get': 'list'})),

#     path('regions/<int:pk>/', RegionViewSet.as_view({'get': 'retrieve'})),

#     path('regions/<int:region_pk>/cities/', CityViewSet.as_view({'get': 'list'})),
#     path('regions/<slug:region_code>/cities/', CityViewSet.as_view({'get': 'list'})),
#     path('countries/<slug:country_code>/cities/', CityViewSet.as_view({'get': 'list'})),

#     path('cities/<int:pk>/', CityViewSet.as_view({'get': 'retrieve'})),
# ]
