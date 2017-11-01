from django.core.management.base import BaseCommand
from django.core.management import call_command

# More serious problems will be checked first
# Here is not used setup_db because we want to preserve the database
# Check_complexity is not used here because it will
# not return error when complexity is high


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        call_command("check")
        call_command("make_db")
        call_command("test_report")
        call_command("check_general")
        call_command("fix_stylesheet")
        call_command("check_stylesheet")

        self.stdout.write(self.style.SUCCESS(
            "\nAll checks runned succesfully :)"
        ))
