import os
import subprocess
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR
from .utils.general import get_modules, apply_to_all_modules, get_script_name


class Command(BaseCommand):

    @staticmethod
    def _call_autopep8(module):
        subprocess.call(['autopep8', '--in-place', '--aggressive',
                         '--aggressive', '--recursive', '--verbose',
                         '--verbose', '--exclude', 'migrations', module])

    def handle(self, *args, **kwargs):
        script_name = get_script_name(__file__)
        apply_to_all_modules(self._call_autopep8, script_name)
