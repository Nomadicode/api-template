import string
import random

from apps.geo.models import Country, Region
from apps.geo.generators import generate_country

def generate_region(
    name=None,
    iso_code=None,
    country=None
):
    if not name:
        name = str.capitalize(''.join(random.choices(string.ascii_lowercase, k=10)))
    
    if not iso_code:
        iso_code = str.upper(name[:2])

    if not country:
        country = generate_country()

    return Region.objects.create(
        name=name,
        iso_code=iso_code,
        country=country
    )

def generate_regions(count=1, country=None):
    regions = []
    for i in range(0, count):
        regions.append(generate_region(country=country))
    
    return regions
