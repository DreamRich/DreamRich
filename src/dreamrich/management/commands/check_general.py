import os
import subprocess
from dreamrich.settings import BASE_DIR
from .utils.general import Checker


class Command(Checker):

    def checker_method(self, module):  # pylint: disable=arguments-differ
        '''
        Check for generals erros using pylint
        '''
        pylintrc_file = os.path.join(BASE_DIR, '.pylintrc')
        returncode = subprocess.call(['pylint', '--rcfile',
                                      pylintrc_file, module])
        return returncode
