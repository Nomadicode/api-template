import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.geo.models import Language


class Command(BaseCommand):
    help = 'Populates the database with languages'

    def handle(self, *args, **options):
        in_file = f"{settings.ROOT_DIR}/seeds/languages.json"

        with open(in_file, 'r') as file:
            data = json.load(file)

            for lang in data:
                Language.objects.get_or_create(**lang)
