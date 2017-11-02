import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from dreamrich.settings import BASE_DIR
from .utils.general import apply_to_all_modules, get_script_name


class Command(BaseCommand):

    @staticmethod
    def _call_pylint(module):
        pylintrc_file = os.path.join(BASE_DIR, '.pylintrc')
        returncode = subprocess.call(['pylint', '--rcfile',
                                      pylintrc_file, module])
        return returncode

    def handle(self, *args, **unused_kwargs):
        script_name = get_script_name(__file__)

        try:
            apply_to_all_modules(self._call_pylint, script_name)
        except CommandError:
            raise CommandError("Pylint found errors in your code")
