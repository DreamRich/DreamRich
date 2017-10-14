# pylint: disable=unused-argument
import os
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Try applying autopep8 fixes")
        path = os.path.realpath(BASE_DIR)
        os.system(
            "autopep8 --exclude=migrations,settings.py,__init__.py" +
            "--inplace --aggressive --recursive '{}'".format(path))
