# pylint: disable=unused-argument
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        path = os.path.realpath(".")
        os.system(
            "autopep8 --exclude=migrations,settings.py,__init__.py -iar %s" %
            path)
