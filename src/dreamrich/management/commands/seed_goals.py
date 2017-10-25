# pylint: disable=unused-argument
import os
import yaml
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR
from goal.models import GoalType


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        file_path = os.path.join(BASE_DIR, 'src', 'dreamrich', 'management',
                                 'seeds', 'goals_seed.yml')

        self.stdout.write('Load seed from {}'.format(file_path))
        with open(file_path, 'r') as element:
            try:
                seed_data = yaml.load(element)
                for registry in seed_data:
                    GoalType.objects.create(**registry)
                    self.stdout.write('Goal type {name} '
                                      'was registered'.format(**registry))
            except yaml.parser.ParserError as parser_error:
                self.stderr.write(str(parser_error))
            except yaml.scanner.ScannerError as scanner_error:
                self.stderr.write(str(scanner_error))
            finally:
                self.stdout.write('End seed')
