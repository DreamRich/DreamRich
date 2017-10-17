# pylint: disable=unused-argument
import os
import yaml
from dreamrich.settings import BASE_DIR


class LoadSeed:

    def __init__(self, file_name, stdout, stderr):
        self.file_name = file_name
        self.stdout = stdout
        self.stderr = stderr

    def _load_path(self):
        return os.path.join(BASE_DIR, 'dreamrich', 'seed',
                            self.file_name)

    def _parse_data(self):
        file_path = self._load_path()
        self.stdout.write('Load seed from {}'.format(file_path))
        with open(file_path, 'r') as seed_content:
            try:
                self.seed_data = yaml.load(seed_content)
            except yaml.parser.ParserError as parser_error:
                self.stderr.write(str(parser_error))
            except yaml.scanner.ScannerError as scanner_error:
                self.stderr.write(str(scanner_error))

    def seeds(self):
        self._parse_data()
        return self.seed_data
