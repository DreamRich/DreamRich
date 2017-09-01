from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        path = os.path.realpath(".")
        self.stdout.write("Raw metrics analysis")
        os.system('{} {}'.format("radon raw {}".format(path),
                                 " --exclude *__init__.py,*management,"
                                 "manage.py,*migrations"))
        self.stdout.write("Analysis complexity")
        message = "radon cc {}".format(path)
        os.system("{} {}".format(message, "--average --exclude *__init__.py,"
                                 "*management,manage.py,*migrations"))
