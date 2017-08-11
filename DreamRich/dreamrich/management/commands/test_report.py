from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Executing tests")
        os.system("coverage run manage.py test")
        self.stdout.write("Loading results")
        os.system("coverage report --show-missing")
