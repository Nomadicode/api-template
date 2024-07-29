import csv
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.geo.models import Country, Region, City


class Command(BaseCommand):
    help = 'Populates the database with cities'

    def handle(self, *args, **options):
        in_file = f"{settings.ROOT_DIR}/seeds/city_seed.csv"

        with open(in_file, 'r') as file:
            csvReader = csv.reader(file)
            headers = next(csvReader)

            for row in csvReader:
                row_data = {key: value for key, value in zip(headers, row)}

                try:
                    country = Country.objects.get(iso_code_2=row_data['country_code'])
                except Country.DoesNotExist:
                    country = None
                    print("Unable to insert, add country: ", row_data["country_code"], row_data["country_name"])
                    continue

                try:
                    region = Region.objects.get(iso_code=row_data['state_code'], country=country)
                except Region.DoesNotExist:
                    region = None

                city, created = City.objects.get_or_create(
                    country=country,
                    region=region,
                    name=row_data["name"],
                    latitude=Decimal(row_data["latitude"]),
                    longitude=Decimal(row_data["longitude"])
                )
