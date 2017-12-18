import os
import subprocess
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        path = os.path.abspath(__file__)
        path = os.path.dirname(path)

        load_scripts = subprocess.Popen(['find', path, '-maxdepth', '1',
                                         '-name', 'load_*'],
                                        stdout=subprocess.PIPE)

        ls_error = load_scripts.wait()

        if not ls_error:
            # Get list of paths scripts
            scripts, _ = load_scripts.communicate()
            scripts = scripts.decode('utf-8')
            scripts = scripts.split('\n')

            scripts.pop(scripts.index(__file__))  # Remove this file

            # Get scripts names from paths
            scripts = [script.rpartition('/')[2] for script in scripts]
            scripts = [script.rpartition('.')[0] for script in scripts]
            scripts = [script for script in scripts if script]

            for script in scripts:
                call_command(script)

            self.stdout.write(self.style.SUCCESS(
                "\nAll loads runned succesfully :)"
            ))
        else:
            raise CommandError(
                "ls command failed to get load scripts"
            )
