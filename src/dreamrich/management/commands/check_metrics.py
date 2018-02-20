import subprocess
from .utils.general import Checker


class Command(Checker):

    exclude_command = ['--ignore', 'manage.py,__init__.py,migrations']

    def checker_method(self, module):
        returncode = subprocess.call(
            ['radon', 'raw', module] + self.exclude_command
        )
        return returncode
