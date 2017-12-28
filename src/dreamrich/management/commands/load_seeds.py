from django.core.management.base import BaseCommand
from django.core.management import call_command
from employee.models import FinancialAdviser


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        self._create_user()
        self.stdout.write("Load active type...")
        call_command("load_active_types")

        self.stdout.write("Load cost types...")
        call_command("load_cost_types")

        self.stdout.write("Load goal types...")
        call_command("load_goal_types")

        self.stdout.write("Load regions...")
        call_command("load_regions")

    def _create_user(self):
        user, _ = FinancialAdviser.objects.get_or_create(
            username="05569807195",
            cpf='05569807195')
        user.set_password('a')
        user.save()
        self.stdout.write("Create a default user...")
