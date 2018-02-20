import subprocess
from .utils.general import Checker


class Command(Checker):

    exclude_command = ['--ignore', 'manage.py,__init__.py,migrations']

    def checker_method(self, module):  # pylint: disable=arguments-differ
        returncode = subprocess.call(
            ['radon', 'cc', '--average', module] + self.exclude_command
        )
        return returncode
