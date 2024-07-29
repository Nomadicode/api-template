import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.geo.models import Continent


class Command(BaseCommand):
    help = 'Populates the database with continents'

    def handle(self, *args, **options):
        in_file = f"{settings.ROOT_DIR}/seeds/continents.json"

        with open(in_file, 'r') as file:
            data = json.load(file)

            for continent in data:
                Continent.objects.get_or_create(**continent)
