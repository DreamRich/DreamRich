from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Erase last coverage analysis")
        os.system("coverage erase")
        self.stdout.write("Executing tests")
        os.system("coverage run manage.py test")
        self.stdout.write("Generating html report")
        os.system("coverage html")
        path = os.path.realpath(".")
        message = "Open the link in your browser\n\tfile:///{}/htmlcov/index.h"\
            "tml".format(path)
        self.stdout.write(message)
