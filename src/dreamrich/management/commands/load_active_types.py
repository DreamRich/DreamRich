from django.core.management.base import BaseCommand
from patrimony.models import ActiveType
from .utils.load_general import load_seed


class Command(BaseCommand):
    @staticmethod
    def _seed_active_types(active_types):
        for active_type in active_types:
            ActiveType.objects.get_or_create(
                **active_type)
            print('\tActive type {name} was registered'
                  .format(**active_type))

    def handle(self, *args, **unused_kwargs):
        load_seed('active_types_seed.yml', self._seed_active_types)
