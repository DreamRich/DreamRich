import yaml
from django.core.management.base import BaseCommand
from goal.models import GoalType

FILE_PATH = 'dreamrich/management/commands/data/goal_type.yaml'

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open(FILE_PATH, 'r') as f:
            seed_data = yaml.load(f)
            for registry in seed_data:
                GoalType.objects.create(**registry)
