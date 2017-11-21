from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        self.stdout.write("Reseting database...")
        call_command("reset_db")

        self.stdout.write("Creating database...")
        call_command("make_db")

        self.stdout.write("Seeding database...")
        call_command("load_db")
