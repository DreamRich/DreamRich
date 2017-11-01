import os
from sys import stderr
import yaml
from dreamrich.settings import BASE_DIR


def load_seed(seed_file_name, seed_function):
    file_path = os.path.join(BASE_DIR, 'src', 'dreamrich',
                             'seeds', seed_file_name)

    print('Load seed from {}'.format(file_path))
    with open(file_path) as load_file:
        try:
            data = yaml.load(load_file)
            seed_function(data)
        except yaml.parser.ParserError as parser_error:
            print(str(parser_error), file=stderr)
        except yaml.scanner.ScannerError as scanner_error:
            print(str(scanner_error), file=stderr)
        finally:
            print('End seed', file=stderr)
