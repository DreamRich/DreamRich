from patrimony.models import ActiveType
from .utils.general import Seeder


class Command(Seeder):
    seed_file_path = 'active_types_seed.yml'

    def seeder_function(self, data):
        for active_type in data:
            ActiveType.objects.get_or_create(**active_type)
            print("\tActive type '{name}' was registered"
                  .format(**active_type))
