import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.geo.models import Country, Region


class Command(BaseCommand):
    help = 'Populates the database with regions/states'

    def handle(self, *args, **options):
        in_file = f"{settings.ROOT_DIR}/seeds/region_seed.csv"

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

                region, created = Region.objects.get_or_create(
                    country=country,
                    name=row_data["name"],
                    iso_code=row_data["state_code"]
                )
