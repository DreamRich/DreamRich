import subprocess
from django.core.management.base import BaseCommand
from .utils.general import apply_to_all_modules, get_script_name


class Command(BaseCommand):

    @staticmethod
    def _call_autopep8(module):
        returncode = subprocess.call(['autopep8', '--in-place',
                                      '--aggressive', '--aggressive',
                                      '--recursive', '--verbose', '--verbose',
                                      '--exclude', 'migrations', module])
        return returncode

    def handle(self, *args, **unused_kwargs):
        script_name = get_script_name(__file__)
        apply_to_all_modules(self._call_autopep8, script_name)
