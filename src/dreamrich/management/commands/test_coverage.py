import os
import subprocess
from dreamrich.settings import BASE_DIR
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **unused_kwargs):
        manage_path = os.path.join(BASE_DIR, 'manage.py')

        self.stdout.write("Erasing last coverage analysis...")
        subprocess.call(['coverage', 'erase'])

        self.stdout.write("Executing tests...")
        subprocess.call(['coverage', 'run', manage_path, 'test'])

        self.stdout.write("Generating html report...")
        subprocess.call(['coverage', 'html'])

        htmlcov_path = os.path.join('src', 'dreamrich', 'management')
        message = ("Open the following link in your browser:\n"
                   "\tfile:///{}/htmlcov/index.html").format(htmlcov_path)
        self.stdout.write(message)
