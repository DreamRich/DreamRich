from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        self.stdout.write("Drop existent database")
        call_command("reset_db")

        self.stdout.write("Make migrations")
        call_command("makemigrations")

        self.stdout.write("Migrate models")
        call_command("migrate")
