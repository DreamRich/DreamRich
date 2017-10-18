# pylint: disable=unused-argument
import os
import subprocess
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR
from .utils.get_modules import get_modules_list


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Executing stylesheet verification")

        src_folder = BASE_DIR + '/'
        pylintrc_file = src_folder + '../.pylintrc'

        apps = get_modules_list()

        self.stdout.write('The folowing modules will be verified: {}'
                          .format(', '.join(apps)))

        for app in apps:
            self.stdout.write('Scanning app {}...'.format(app))
            app = src_folder + app

            subprocess.call(['pylint', '--rcfile', pylintrc_file, app])
