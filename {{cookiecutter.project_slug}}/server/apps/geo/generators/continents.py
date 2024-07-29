import string
import random

from apps.geo.models import Continent


def generate_continent(name=None, iso_code=None):
    if not name:
        name = str.capitalize(''.join(random.choices(string.ascii_lowercase, k=10)))
    
    if not iso_code:
        iso_code = str.upper(name[:2])

    return Continent.objects.create(name=name, iso_code=iso_code)

def generate_continents(count=1):
    continents = []
    for i in range(0, count):
        continents.append(generate_continent())
    
    return continents