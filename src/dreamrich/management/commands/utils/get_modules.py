import subprocess


def get_modules_list():
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
    modules = sorted([module for module in modules if len(module)])

    return modules
