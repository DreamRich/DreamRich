# pylint: disable=unused-argument
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Reseting database...")
        call_command("reset_db")

        self.stdout.write("Seeding database...")
        call_command("seed_db")
