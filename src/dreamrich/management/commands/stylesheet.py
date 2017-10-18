# pylint: disable=unused-argument
import os
import subprocess
from django.core.management.base import BaseCommand
from dreamrich.settings import BASE_DIR


class Command(BaseCommand):

    def _get_modules_list(self):
        inits_paths = subprocess.Popen(['find', '-name', '__init__.py'],
                                       stdout=subprocess.PIPE)

        modules = subprocess.Popen(['cut', '-d', '/', '-f', '2'],
                                           stdin=inits_paths.stdout,
                                           stdout=subprocess.PIPE)

        modules, error = modules.communicate()

        if error:
            self.stderr.write("Wasn't possible to run bash" +
                              " commands, probably your environment" +
                              " is not compatible or you don't" + 
                              " have permissions")
            exit(1)

        else:
            modules = modules.decode('utf-8')
            modules = set(modules.split('\n'))

        modules = list(modules)
        modules = [module for module in modules if len(module)]

        return modules

    def handle(self, *args, **kwargs):
        self.stdout.write("Executing stylesheet verification")

        src_folder = BASE_DIR + '/'
        pylintrc_file = src_folder + '../.pylintrc'

        apps = self._get_modules_list()

        self.stdout.write('The folowing modules will be verified: {}'
                          .format(', '.join(apps)))

        for app in apps:
            self.stdout.write('Scanning app {}...'.format(app))

            app = src_folder + app
            subprocess.call(['pylint', '--rcfile', pylintrc_file, app])
