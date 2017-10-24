# pylint: disable=unused-argument
import os
import subprocess
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR
from .utils.general import apply_to_all_modules, get_script_name


class Command(BaseCommand):

    @staticmethod
    def _call_pylint(module):
        pylintrc_file = os.path.join(BASE_DIR, '.pylintrc')
        subprocess.call(['pylint', '--rcfile', pylintrc_file, module])

    def handle(self, *args, **kwargs):
        script_name = get_script_name(__file__)
        apply_to_all_modules(self._call_pylint, script_name)
