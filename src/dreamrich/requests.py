from enum import Enum, auto


class RequestTypes(Enum):

    def _generate_next_value_(self, name, start, count, last_values):
        # pylint: disable=unused-argument
        return name.lower()

    GET = auto()
    GETLIST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()
    POST = auto()
