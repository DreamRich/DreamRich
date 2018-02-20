from client.models import Country, State
from .utils.general import Seeder


class Command(Seeder):
    seed_file_path = 'regions_seed.yml'

    def seeder_function(self, data):
        for country in data:
            states = country.pop('states')

            new_country, _ = Country.objects.get_or_create(**country)
            print("\tCountry '{name} - {abbreviation}'"
                  " was registered".format(**country))

            for state in states:
                State.objects.get_or_create(country=new_country, **state)
                print("\t\tState '{name} - {abbreviation}'"
                      " was registered".format(**state))
