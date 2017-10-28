from django.core.management.base import BaseCommand
from patrimony.models import ActiveType
from .utils.seeds import seed_seed


class Command(BaseCommand):
    @staticmethod
    def _seed_active_types(active_types):
        for active_type in active_types:
            ActiveType.objects.get_or_create(
                **active_type)
            print('Active type {name} was registered'
                  .format(**type_cost))

    def handle(self, *args, **unused_kwargs):
        seed_seed('cost_types_seed.yml', self._seed_cost_types)
