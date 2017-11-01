import subprocess
from django.core.management.base import BaseCommand, CommandError
from .utils.general import apply_to_all_modules, get_script_name


class Command(BaseCommand):

    @staticmethod
    def _call_pycodestyle(module):
        returncode = subprocess.call(['pycodestyle', '--statistics', '--count',
                                      '--exclude', 'migrations', module])
        return returncode

    def handle(self, *args, **unused_kwargs):
        script_name = get_script_name(__file__)

        try:
            apply_to_all_modules(self._call_pycodestyle, script_name)
        except CommandError:
            raise CommandError("There are stylesheet problems in your code")
