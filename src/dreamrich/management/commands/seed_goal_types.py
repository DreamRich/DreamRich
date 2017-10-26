from django.core.management.base import BaseCommand
from goal.models import GoalType
from .utils.seeds import seed_seed


class Command(BaseCommand):

    @staticmethod
    def _seed_goal_types(goal_types):
        for goal_type in goal_types:
            GoalType.objects.create(**goal_type)
            print('Goal {name} was registered'
                  .format(**goal_type))

    def handle(self, *args, **unused_kwargs):
        seed_seed('goal_types_seed.yml', self._seed_goal_types)
