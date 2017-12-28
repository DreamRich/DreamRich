from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        self.stdout.write("Reseting database...")
        call_command("make_db")

        self.stdout.write("Load seeds...")
        call_command("load_seeds")
