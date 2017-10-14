# pylint: disable=unused-argument
import os
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Executing stylesheet verification")
        path = os.path.realpath(BASE_DIR)
        os.system("pylint --load-plugins pylint_django '{}'".format(path))
