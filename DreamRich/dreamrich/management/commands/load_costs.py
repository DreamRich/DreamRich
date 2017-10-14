# pylint: disable=unused-argument
import os
import yaml
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR
from financial_planning.models import CostType


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        file_path = os.path.join(BASE_DIR, 'dreamrich', 'seed',
                                 'cost_types_data.yml')

        self.stdout.write('Load seed from {}'.format(file_path))
        with open(file_path) as load_file:
            try:
                types = yaml.load(load_file)
                for type_cost in types:
                    CostType.objects.get_or_create(
                        **type_cost)
                    self.stdout.write('Cost type {name} '
                                      'was registered'.format(**type_cost))
            except yaml.parser.ParserError as parser_error:
                self.stderr.write(str(parser_error))
            except yaml.scanner.ScannerError as scanner_error:
                self.stderr.write(str(scanner_error))
            finally:
                self.stdout.write('End seed')
