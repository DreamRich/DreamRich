from django.core.management.base import BaseCommand
from client.models import Country, State
from .utils.load_general import load_seed


class Command(BaseCommand):
    @staticmethod
    def _seed_regions(regions):
        for country in regions:
            states = country.pop('states', [])

            new_country, _ = Country.objects.get_or_create(
                **country)
            print('\tCountry {name} - {abbreviation}'
                  ' was registered'.format(**country))

            for state in states:
                State.objects.get_or_create(country=new_country,
                                            **state)
                print('\t\tState {name} - {abbreviation}'
                      ' was registered'.format(**state))

    def handle(self, *args, **unused_kwargs):
        load_seed('regions_seed.yml', self._seed_regions)
