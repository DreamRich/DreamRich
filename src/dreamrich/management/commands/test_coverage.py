# pylint: disable=unused-argument
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Erase last coverage analysis")
        os.system("coverage erase")
        self.stdout.write("Executing tests")
        os.system("coverage run manage.py test")
        self.stdout.write("Generating html report")
        os.system("coverage html")
        path = os.path.realpath(".")
        message = "Open the link in your browser\n\tfile:///{}/\
                   htmlcov/index.html".format(path)
        self.stdout.write(message)
