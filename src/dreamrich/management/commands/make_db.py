from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        self.stdout.write("Making migrations...")
        call_command("makemigrations")

        self.stdout.write("Migrating database...")
        call_command("migrate")
