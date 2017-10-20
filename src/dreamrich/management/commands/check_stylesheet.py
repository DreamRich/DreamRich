# pylint: disable=unused-argument
import os
import subprocess
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR
from .utils.get_modules import get_modules


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Executing stylesheet verification")

        src_folder = BASE_DIR + '/'

        apps = get_modules()

        self.stdout.write('The folowing modules will be verified: {}'
                          .format(', '.join(apps)))

        for app in apps:
            self.stdout.write('Scanning app {}...'.format(app))
            app = src_folder + app

            returncode = subprocess.call(['pycodestyle', '--statistics', '--count',
                             '--exclude', 'migrations', app])

            has_error = True if returncode else False

        if has_error:
            exit(1)
