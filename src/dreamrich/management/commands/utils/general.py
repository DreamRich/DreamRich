import os
import subprocess
from django.core.management.base import CommandError
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
    cut_return_code = remove_leading.wait()

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
    on
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
