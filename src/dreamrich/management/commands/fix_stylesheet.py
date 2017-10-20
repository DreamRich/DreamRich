import os
import subprocess
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR
from .utils.get_modules import get_modules_list


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Executing autofix verification autopep8 fixes...")

        src_folder = BASE_DIR + '/'
        apps = get_modules_list()

        self.stdout.write('The folowing module will be fixed: {}'
                          .format(', '.join(apps)))

        for app in apps:
            self.stdout.write("Applying autofix on app {}...".format(app))
            app = src_folder + app

            subprocess.call(['autopep8', '--in-place', '--aggressive',
                             '--aggressive', '--recursive', '--verbose',
                             '--verbose', '--exclude', 'migrations', app])
