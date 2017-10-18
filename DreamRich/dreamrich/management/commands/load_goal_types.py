# pylint: disable=unused-argument
from django.core.management.base import BaseCommand
from dreamrich.management.commands.loads import LoadSeed
from goal.models import GoalType


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        loader_seed = LoadSeed('cost_types_data.yml', self.stdout, self.stderr)

        for goal_type in loader_seed.seeds():
            GoalType.objects.get_or_create(**goal_type)
            self.stdout.write('Goal type {name} '
                              'was registered'.format(**goal_type))
