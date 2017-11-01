import inspect
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from dreamrich.settings import LOCAL_APPS
from employee.models import FinancialAdviser


class Command(BaseCommand):
    level = 0
    loops = 3

    def handle(self, *args, **kwargs):
        self._create_user()

        self._print_message("Loading apps")
        self.level += 1
        self.loops = kwargs['loop']
        for app in LOCAL_APPS:
            try:
                self._print_message("Load app({}) module".format(app))
                app_module = __import__("{}.factories".format(app)).factories
                # self._print_message("{} has factories :) ".format(app))
                self.level += 1
                self._load_factories(app_module, app)
                self.level -= 1
            except AttributeError:
                self.level += 1
                self._print_error("{} don't have factories :( ".format(app))
                self.level -= 1
            except ImportError:
                self.level += 1
                self._print_error("{} factory module not found D:".format(app))
                self.level -= 1

    def _create_user(self):
        user, _ = FinancialAdviser.objects.get_or_create(
            username="12312312387",
            cpf='12312312387')
        user.set_password('a')
        user.save()
        self._print_message(
            'Creating a default user(username: 12312312387 password: a)')

    def _load_factories(self, app_module, app):
        has_main = False
        for name, obj in inspect.getmembers(app_module):
            has_main |= name.find('MainFactory') != -1
            if inspect.isclass(obj) and name.find('MainFactory') != -1:
                self._print_message("Creating objects to {}".format(name))
                self.level += 1
                self._create_objects(obj)
                self.level -= 1
        if not has_main:
            self._print_error("{} does not have MainFactory".format(app))

    def _create_objects(self, obj):
        loop = 0
        error_message = "\n{}".format("  " * self.level)
        self._print_message("", ending="")
        while loop < self.loops:
            try:
                getattr(obj, 'create')()
                self._print_message("$", ending="", level=0)
                loop += 1
            except IntegrityError as error:
                error_message += "{}, ".format(error)
        self.stdout.write("")
        self._print_error(error_message)

    def _print_message(self, message, *args, **kwargs):
        level = kwargs.pop('level', self.level)
        self.stdout.write("{}{}".format("  " * level, message),
                          *args, **kwargs)
        self.stdout.flush()

    def _print_error(self, message, *args, **kwargs):
        self.stderr.write("{}{}".format("  " * self.level, message),
                          *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            type=int,
            dest='loop',
            default=3,
            help='The number of each class to be created'
        )
