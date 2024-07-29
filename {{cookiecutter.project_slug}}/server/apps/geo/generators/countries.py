import string
import random

from apps.geo.models import Country
from apps.geo.generators import generate_continent

def generate_country(
    name=None,
    iso_code_2=None,
    iso_code_3=None,
    numeric_code=None,
    continent=None
):
    if not name:
        name = str.capitalize(''.join(random.choices(string.ascii_lowercase, k=10)))
    
    if not iso_code_2:
        iso_code_2 = str.upper(name[:2])

    if not iso_code_3:
        iso_code_3 = str.upper(name[:3])

    if not numeric_code:
        numeric_code = int(''.join(random.choices(string.digits, k=3)))

    if not continent:
        continent = generate_continent()

    return Country.objects.create(
        name=name,
        iso_code_2=iso_code_2,
        iso_code_3=iso_code_3,
        numeric_code=numeric_code,
        continent=continent
    )

def generate_countries(count=1, continent=None):
    countries = []
    for i in range(0, count):
        countries.append(generate_country(continent=continent))
    
    return countries