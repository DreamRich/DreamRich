from django.core.management.base import BaseCommand
from goal.models import GoalType
from .utils.load_general import load_seed


class Command(BaseCommand):

    @staticmethod
    def _seed_goal_types(goal_types):
        for goal_type in goal_types:
            GoalType.objects.create(**goal_type)
            print('\tGoal {name} was registered'
                  .format(**goal_type))

    def handle(self, *args, **unused_kwargs):
        load_seed('goal_types_seed.yml', self._seed_goal_types)
