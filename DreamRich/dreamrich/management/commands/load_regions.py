# pylint: disable=unused-argument
from django.core.management.base import BaseCommand
from dreamrich.management.commands.loads import LoadSeed
from client.models import Country, State


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        seed_loader = LoadSeed('regions_data_list.yml', self.stdout,
                               self.stderr)

        for country in seed_loader.seeds():
            states = country.pop('states', [])
            new_country, _ = Country.objects.get_or_create(**country)
            self.stdout.write('\tCountry {name} - {abbreviation} '
                              'was registered'.format(**country))

            for state in states:
                State.objects.get_or_create(country=new_country, **state)
                self.stdout.write('\t\tState {name} - {abbreviation} '
                                  'was registered'.format(**state))
