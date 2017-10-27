# pylint: disable=unused-argument
from django.core.management.base import BaseCommand
from dreamrich.management.commands.loads import LoadSeed
from patrimony.models import ActiveType


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        seed_loader = LoadSeed('active_types_data.yml', self.stdout, self.stderr)
        for active_type in seed_loader.seeds():
            ActiveType.objects.get_or_create(
                **active_type)
            self.stdout.write('Active type {name} '
                              'was registered'.format(**active_type))
