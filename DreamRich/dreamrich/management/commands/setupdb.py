# pylint: disable=unused-argument
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        call_command("resetdb")
        self.stdout.write("Execute seed")
        call_command("seed")
