import subprocess
from django.core.management.base import BaseCommand
from .utils.general import apply_to_all_modules, get_script_name

EXCLUDE_COMMAND = ['--ignore', 'manage.py,__init__.py,migrations']


class Command(BaseCommand):

    @staticmethod
    def _call_radon_raw(module):
        returncode = subprocess.call(
            ['radon', 'raw', module] + EXCLUDE_COMMAND)
        return returncode

    @staticmethod
    def _call_radon_cc(module):
        returncode = subprocess.call(['radon', 'cc', '--average',
                                      module] + EXCLUDE_COMMAND)
        return returncode

    def handle(self, *args, **unused_kwargs):
        script_name = get_script_name(__file__)

        self.stdout.write("Analysing raw metrics...\n")
        apply_to_all_modules(self._call_radon_raw, script_name)

        self.stdout.write("Analysing cyclomatic-complexity")
        apply_to_all_modules(self._call_radon_cc, script_name)
