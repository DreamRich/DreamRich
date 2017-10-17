# pylint: disable=unused-argument
from django.core.management.base import BaseCommand
from dreamrich.management.commands.loads import LoadSeed
from financial_planning.models import CostType


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        seed_loader = LoadSeed('cost_types_data.yml', self.stdout, self.stderr)
        for type_cost in seed_loader.seeds():
            CostType.objects.get_or_create(
                **type_cost)
            self.stdout.write('Cost type {name} '
                              'was registered'.format(**type_cost))
