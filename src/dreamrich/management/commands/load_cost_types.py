from django.core.management.base import BaseCommand
from financial_planning.models import CostType
from .utils.load_general import load_seed


class Command(BaseCommand):
    @staticmethod
    def _seed_cost_types(cost_types):
        for type_cost in cost_types:
            CostType.objects.get_or_create(
                **type_cost)
            print('\tCost type {name} was registered'
                  .format(**type_cost))

    def handle(self, *args, **unused_kwargs):
        load_seed('cost_types_seed.yml', self._seed_cost_types)
