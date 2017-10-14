# pylint: disable=unused-argument
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Try apply autopep8 fixes")
        path = os.path.realpath(".")
        os.system(
            "autopep8 --exclude=migrations,settings.py,__init__.py -iar %s" %
            path)
