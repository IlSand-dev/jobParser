from django.core.management.base import BaseCommand
from vacancy.models import *
import requests
from vacancy.hhAPI import *


class Command(BaseCommand):
    help = 'Load currency from hh.ru'

    def handle(self, *args, **options):
        for currency in load_currency():
            Currency(code=currency['code'], abbr=currency['abbr']).save()
