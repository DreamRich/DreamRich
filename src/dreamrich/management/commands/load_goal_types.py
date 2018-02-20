from goal.models import GoalType
from .utils.general import Seeder


class Command(Seeder):
    seed_file_path = 'goal_types_seed.yml'

    def seeder_function(self, data):
        for goal_type in data:
            GoalType.objects.create(**goal_type)
            print("\tGoal '{name}' was registered".format(**goal_type))
