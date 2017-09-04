# pylint: disable=unused-argument
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        path = os.path.realpath(".")
        self.stdout.write("Executing stylesheet verification")
        os.system("pylint --load-plugins pylint_django {}".format(path))
