import subprocess
import os
from dreamrich.settings import BASE_DIR
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        manage_path = os.path.join(BASE_DIR, 'manage.py')

        self.stdout.write("Executing tests...")
        subprocess.call(['coverage', 'run', manage_path, 'test'])

        self.stdout.write("Loading results...")
        subprocess.call(['coverage', 'report', '--show-missing'])
