import inspect
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from dreamrich import complete_factories
from employee.models import FinancialAdviser


class Command(BaseCommand):
    level = 0
    loops = 3

    def handle(self, *args, **kwargs):
        self._create_user()

        self._print_message("Loading apps")
        self.level += 1
        self.loops = kwargs['loop']

        self.level += 1
        self._load_factories()
        self.level -= 1

    def _create_user(self):
        user, _ = FinancialAdviser.objects.get_or_create(
            username="12312312387",
            cpf='12312312387'
        )
        user.set_password('a')
        user.save()
        self._print_message(
            'Creating a default user(username: 12312312387 password: a)'
        )

    def _load_factories(self):
        module_objects = inspect.getmembers(complete_factories)

        factories = [
            obj for obj in module_objects if inspect.isclass(obj[1])
            and obj[0].find('CompleteFactory') != -1
        ]

        for name, cls in factories:
            self._print_message("Creating objects from '{}'".format(name))
            self.level += 1
            self._create_objects(cls)
            self.level -= 1

    def _create_objects(self, factory):
        loop = 0

        error_message = "\n{}".format("  " * self.level)
        self._print_message("", ending="")

        while loop < self.loops:
            try:
                create_method = getattr(factory, 'create')
                create_method()

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
