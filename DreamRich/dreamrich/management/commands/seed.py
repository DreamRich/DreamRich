import inspect
from django.core.management.base import BaseCommand
from dreamrich.settings import LOCAL_APPS


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for app in LOCAL_APPS:
            try:
                self.stdout.write("Load app({}) module".format(app))
                app_module = __import__("{}.factories".format(app)).factories
                self.stdout.write("{} has factories :) ".format(app))
                for name, obj in inspect.getmembers(app_module):
                    if inspect.isclass(obj) and name.find('MainFactory') != -1:
                        self.stdout.write("Creating objects to {}".format(app))
                        for n in range(kwargs['loop']):
                            getattr(obj, 'create')()
                            self.stdout.write(".", ending="")
            except AttributeError:
                self.stderr.write("{} don't have factories :( ".format(app))

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            type=int,
            dest='loop',
            default=3,
            help='The number of each class to be created'
        )
