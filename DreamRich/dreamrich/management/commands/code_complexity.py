from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        path = os.path.realpath(".")
        self.stdout.write("Raw metrics analysis")
        os.system(
            "radon raw {} --exclude *__init__.py,*management,manage.py,*migrations".format(path))
        self.stdout.write("Analysis complexity")
        os.system(
            "radon cc {} --average --exclude *__init__.py,*management,manage.py,*migrations".format(path))
