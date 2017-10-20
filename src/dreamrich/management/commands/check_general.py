# pylint: disable=unused-argument
import os
import subprocess
from django.core.management.base import BaseCommand
from .utils.general import get_modules, apply_to_all_modules, get_script_name
from dreamrich.settings import BASE_DIR


class Command(BaseCommand):

    @staticmethod
    def _call_pylint(module):
        pylintrc_file = os.path.join(BASE_DIR, '../.pylintrc')
        subprocess.call(['pylint', '--rcfile', pylintrc_file, module])

    def handle(self, *args, **kwargs):
        script_name = get_script_name(__file__)
        apply_to_all_modules(self._call_pylint, script_name)
