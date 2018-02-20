import os
import subprocess
import yaml
from django.core.management.base import BaseCommand, CommandError
from dreamrich.settings import BASE_DIR


SRC_FOLDER = os.path.join(BASE_DIR, 'src')


# Cannot use same logic that load_all.py because there can be nested modules
def get_modules():
    get_abs_paths = subprocess.Popen(['find', SRC_FOLDER, '-name',
                                      '__init__.py'], stdout=subprocess.PIPE)
    find_return_code = get_abs_paths.wait()

    remove_leading = subprocess.Popen(['sed', 's@{}@@'.format(SRC_FOLDER)],
                                      stdin=get_abs_paths.stdout,
                                      stdout=subprocess.PIPE)
    sed_return_code = remove_leading.wait()

    remove_trailing = subprocess.Popen(['cut', '-d', '/', '-f', '2'],
                                       stdin=remove_leading.stdout,
                                       stdout=subprocess.PIPE)
    cut_return_code = remove_trailing.wait()

    modules, _ = remove_trailing.communicate()

    if not find_return_code and not sed_return_code and not cut_return_code:
        modules = modules.decode('utf-8')
        modules = set(modules.split('\n'))

        modules = list(modules)
        modules = sorted([module for module in modules if len(module)])

        return modules
    else:
        raise CommandError(
            "Some bash command returned an error, is not possible to get"
            " the modules list."
            "\nfind_return_code: {}"
            "\nsed_return_code: {}"
            "\ncut_return_code: {}".format(
                find_return_code,
                sed_return_code,
                cut_return_code
            )
        )


def get_script_name(path):
    script_name = os.path.basename(path)
    script_name = os.path.splitext(script_name)[0]  # Remove extension

    return script_name


def apply_to_all_modules(function, script_name):
    """ Apply a function to all modules.
    :param function: Must receive just one parameter, the module name and
    the module that must be located on src folder
    """
    print("\nApplying {}...\n".format(script_name))

    modules = get_modules()

    print('{} will be applied on the following modules: {}'
          .format(script_name, ', '.join(modules)))

    has_error = False
    for module in modules:
        print('\nApplying {} to module {}...'.format(script_name, module))
        module = os.path.join(SRC_FOLDER, module)

        returncode = function(module)
        has_error = True if returncode or has_error else False

    if has_error:
        raise CommandError("Error while applying {}".format(script_name))


class Checker(BaseCommand):

    def checker_method(self, module):
        raise NotImplemented('This method must be implemented'
                             ' on children classes')

    def handle(self, *args, **unused_kwargs):
        script_name = get_script_name(__file__)

        try:
            apply_to_all_modules(self.checker_method, script_name)
        except CommandError:
            raise CommandError("Pylint found errors in your code")


class Seeder(BaseCommand):
    seed_file_path = ''

    def seeder_function(self, data):
        raise NotImplemented('This method must be implemented'
                             ' on child classes')

    def load_seed(self, seed_file_name, seed_function):
        file_path = os.path.join(BASE_DIR, 'src', 'dreamrich',
                                 'seeds', seed_file_name)

        print("Processing seed from '{}'...".format(file_path))
        with open(file_path) as load_file:
            try:
                data = yaml.load(load_file)
                seed_function(data)
            except (yaml.parser.ParserError, yaml.scanner.ScannerError):
                raise CommandError(
                    "Couldn't process seed '{}'".format(file_path)
                )

        print('Finish processing seed')

    def handle(self, *args, **unused_kwargs):
        if self.seed_file_path:
            self.load_seed(self.seed_file_path, self.seeder_function)
        else:
            raise AttributeError("'seed_file_path' must be filled on child"
                                 " classes")
