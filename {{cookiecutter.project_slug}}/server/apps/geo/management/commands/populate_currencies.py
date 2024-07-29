import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.geo.models import Currency


class Command(BaseCommand):
    help = 'Populates the database with currencies'

    def handle(self, *args, **options):
        in_file = f"{settings.ROOT_DIR}/seeds/currencies.json"

        with open(in_file, 'r') as file:
            data = json.load(file)

            for currency in data:
                Currency.objects.get_or_create(**currency)
