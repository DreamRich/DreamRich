import os
import sys
import subprocess
from dreamrich.settings import BASE_DIR


def get_modules():
    inits_paths = subprocess.Popen(['find', 'src', '-name', '__init__.py'],
                                   stdout=subprocess.PIPE)

    modules = subprocess.Popen(['cut', '-d', '/', '-f', '2'],
                               stdin=inits_paths.stdout,
                               stdout=subprocess.PIPE)

    modules, error = modules.communicate()

    if error:
        print("Wasn't possible to run bash" +
              " commands, probably your environment" +
              " is not compatible or you don't" +
              " have permissions", file=sys.stderr)

        exit(1)

    else:
        modules = modules.decode('utf-8')
        modules = set(modules.split('\n'))

        modules = list(modules)
        modules = sorted([module for module in modules if len(module)])

        return modules


def get_script_name(path):
    script_name = os.path.basename(path)
    script_name = os.path.splitext(script_name)[0]  # Remove extension

    return script_name


def apply_to_all_modules(function, script_name):
    """ Apply a function to all modules.
    :param function: Must receive just one parameter, the module name and
    the module that must be located on src folder
    on
    """
    print("\nApplying {}...\n".format(script_name))

    modules = get_modules()

    print('{} will be applied on the following modules: {}'
          .format(script_name, ', '.join(modules)))

    for module in modules:
        print('\nApplying {} to module {}...'.format(script_name, module))
        module = os.path.join(BASE_DIR, 'src', module)

        returncode = function(module)
        has_error = True if returncode else False

    if has_error:
        exit(1)
