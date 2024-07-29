import string
import random
import decimal

from apps.geo.models import Country, Region, City
from apps.geo.generators import generate_country, generate_region

def generate_city(
    name=None,
    latitude=None,
    longitude=None,
    country=None,
    region=None
):
    if not name:
        name = str.capitalize(''.join(random.choices(string.ascii_lowercase, k=10)))
    
    if not latitude:
        latitude = decimal.Decimal(random.randrange(-180, 180))

    if not longitude:
        longitude = decimal.Decimal(random.randrange(-90, 90))

    if region and not country:
        country = region.country

    if country and not region:
        region = generate_region(country=country)
    
    if not country and not region:
        country = generate_country()
        region = generate_region(country=country)

    return City.objects.create(
        name=name,
        latitude=latitude,
        longitude=longitude,
        country=country,
        region=region
    )

def generate_cities(count=1, country=None, region=None):
    cities = []
    for i in range(0, count):
        cities.append(generate_city(country=country, region=region))
    
    return cities
