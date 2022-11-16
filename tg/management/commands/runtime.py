from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Run cron api'

    def handle(self, *args, **options):
        from config import operator

        operator.start()
