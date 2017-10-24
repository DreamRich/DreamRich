# pylint: disable=unused-argument
import subprocess
from django.core.management.base import BaseCommand
from .utils.general import apply_to_all_modules, get_script_name


class Command(BaseCommand):

    @staticmethod
    def _call_pycodestyle(module):
        returncode = subprocess.call(['pycodestyle', '--statistics', '--count',
                                      '--exclude', 'migrations', module])
        return returncode

    def handle(self, *args, **kwargs):
        script_name = get_script_name(__file__)
        apply_to_all_modules(self._call_pycodestyle, script_name)
