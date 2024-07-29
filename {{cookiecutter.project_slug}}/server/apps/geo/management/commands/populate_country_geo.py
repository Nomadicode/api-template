import json

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.geo.models import Country

DEFAULT_MAPPED_REGIONS = [
    "Antarctica",
    "Africa",
    "Asia",
    "Europe",
    "Oceania"
]

CONTINENT_MAP = {
    "Northern America": "North America",
    "Caribbean": "North America",
    "Central America": "North America",
    "South America": "South America"
}


class Command(BaseCommand):
    help = 'Populates the database with countries'

    def handle(self, *args, **options):
        geo_file = f"{settings.ROOT_DIR}/seeds/countries.geojson"
        geo_data = open(geo_file, 'r').read()
        geo_json = json.loads(geo_data)
        features = geo_json["features"]

        countries = Country.objects.all()

        for country in countries:
            country_features = [feat for feat in features if feat['properties']['ISO_CC'].lower() == country.iso_code_3.lower()]
            print(country_features)

            break