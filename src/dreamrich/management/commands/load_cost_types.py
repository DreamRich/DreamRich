from financial_planning.models import CostType
from .utils.general import Seeder


class Command(Seeder):
    seed_file_path = 'cost_types_seed.yml'

    def seeder_function(self, data):
        for type_cost in data:
            CostType.objects.get_or_create(**type_cost)
            print("\tCost type '{name}' was registered".format(**type_cost))
