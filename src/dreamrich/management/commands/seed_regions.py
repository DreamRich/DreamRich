# pylint: disable=unused-argument
import os
import yaml
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR
from client.models import Country, State


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        file_path = os.path.join(BASE_DIR, 'src', 'dreamrich', 'management',
                                 'seeds', 'regions_seed.yml')

        self.stdout.write('Load seed from {}'.format(file_path))
        with open(file_path) as load_file:
            try:
                data = yaml.load(load_file)
                for country in data:
                    states = country.pop('states', [])

                    new_country, _ = Country.objects.get_or_create(
                        **country)
                    self.stdout.write('\tCountry {name} - {abbreviation} '
                                      'was registered'.format(**country))

                    for state in states:
                        State.objects.get_or_create(country=new_country,
                                                    **state)
                        self.stdout.write('\t\tState {name} - {abbreviation} '
                                          'was registered'.format(**state))

            except yaml.parser.ParserError as parser_error:
                self.stderr.write(str(parser_error))
            except yaml.scanner.ScannerError as scanner_error:
                self.stderr.write(str(scanner_error))
            finally:
                self.stdout.write('End seed')
