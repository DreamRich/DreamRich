# pylint: disable=unused-argument
from django.core.management.base import BaseCommand
from financial_planning.models import CostType
from .utils.seeds import seed_seed


class Command(BaseCommand):
    @staticmethod
    def _seed_cost_types(cost_types):
        for type_cost in cost_types:
            CostType.objects.get_or_create(
                **type_cost)
            print('Cost type {name} was registered'
                  .format(**type_cost))


    def handle(self, *args, **kwargs):
        seed_seed('cost_types_seed.yml', self._seed_cost_types)
