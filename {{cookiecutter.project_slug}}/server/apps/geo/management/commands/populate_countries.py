import json

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.geo.models import Country, Continent, Currency, Language

# DEFAULT_MAPPED_REGIONS = [
#     "Antarctica",
#     "Africa",
#     "Asia",
#     "Europe",
#     "Oceania"
# ]

# CONTINENT_MAP = {
#     "Northern America": "North America",
#     "Caribbean": "North America",
#     "Central America": "North America",
#     "South America": "South America"
# }


class Command(BaseCommand):
    help = 'Populates the database with countries'

    # def handle(self, *args, **options):
    #     in_file = f"{settings.ROOT_DIR}/seeds/country_seed.csv"

    #     with open(in_file, 'r') as file:
    #         csvReader = csv.reader(file)
    #         headers = next(csvReader)

    #         for row in csvReader:
    #             row_data = {key: value for key, value in zip(headers, row)}

    #             if row_data["region"] not in DEFAULT_MAPPED_REGIONS:
    #                 row_data["region"] = CONTINENT_MAP[row_data["subregion"]]

    #             try:
    #                 continent = Continent.objects.get(name=row_data['region'])
    #             except Continent.DoesNotExist:
    #                 continent = None
                
    #             try:
    #                 currency = Currency.objects.get(iso_code=row_data['currency'])
    #             except Currency.DoesNotExist:
    #                 currency = None

    #             country, created = Country.objects.get_or_create(
    #                 continent=continent,
    #                 currency=currency,
    #                 name=row_data["name"],
    #                 iso_code_2=row_data["iso2"],
    #                 iso_code_3=row_data["iso3"],
    #                 numeric_code=row_data["numeric_code"],
    #                 phone_code=row_data["phone_code"]
    #             )

    def handle(self, *args, **options):
        in_file = f"{settings.ROOT_DIR}/seeds/countries.json"

        with open(in_file, 'r') as file:
            data = json.load(file)

            for country in data:
                
                country_data = {
                    "name": country["name"],
                    "iso_code_2": country["iso_code_2"],
                    "iso_code_3": country["iso_code_3"],
                    "numeric_code": country["numeric_code"],
                    "phone_code": country["phone_code"]
                }

                if country["continent_code"]:
                    country_data["continent"] = Continent.objects.get(iso_code=country["continent_code"])

                if country["currency_code"]:
                    try:
                        country_data["currency"] = Currency.objects.get(iso_code=country["currency_code"])
                    except Exception:
                        print(country["currency_code"])

                new_country, created = Country.objects.get_or_create(**country_data)

                if created and len(country["language_codes"]):
                    for lang_code in country["language_codes"]:
                        try:
                            language = Language.objects.get(alpha_2_code=lang_code)
                        except Language.DoesNotExist:
                            print(new_country.name, lang_code)
                            continue

                        new_country.languages.add(language)
