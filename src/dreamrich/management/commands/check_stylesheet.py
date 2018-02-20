import subprocess
from .utils.general import Checker


class Command(Checker):

    def checker_method(self, module):  # pylint: disable=arguments-differ
        returncode = subprocess.call(['pycodestyle', '--statistics', '--count',
                                      '--exclude', 'migrations', module])
        return returncode
