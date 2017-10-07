# pylint: disable=unused-argument
from django.core.management.base import BaseCommand
from client.models import Country, State

FILE_PATH = 'dreamrich/management/commands/data/regions_data_list'


class Command(BaseCommand):
    @staticmethod
    def _parse_line(line):
        # Split on last space and rotate back
        name, abbreviation = line[::-1].split(maxsplit=1)
        name, abbreviation = abbreviation[::-1], name[::-1]

        return name, abbreviation

    def handle(self, *args, **kwargs):
        with open(FILE_PATH) as file:
            for line in file:
                line = line.lstrip()

                if not line:
                    continue

                elif line[0:2] == "->":
                    line = line[3:]  # 3 to take space as well

                    try:
                        country, abbreviation = self._parse_line(line)
                    except ValueError:
                        self.stderr.write('Probably the file format is wrong')

                    Country.objects.create(
                        name=country,
                        abbreviation=abbreviation
                    )
                    self.stdout.write('Country {} - {} was registered'.format(
                        country,
                        abbreviation
                    ))

                else:
                    try:
                        state, abbreviation = self._parse_line(line)
                    except ValueError:
                        self.stderr.write('Probably the file format is wrong')

                    State.objects.create(
                        name=state,
                        abbreviation=abbreviation,
                        country_id=Country.objects.last().id
                    )
                    self.stdout.write('State {} - {} was registered'.format(
                        state,
                        abbreviation
                    ))

            self.stdout.write('\nAll regions were registered successfully!')
