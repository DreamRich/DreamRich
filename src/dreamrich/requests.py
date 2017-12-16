from enum import Enum, auto


class RequestTypes(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    GET = auto()
    GETLIST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()
    POST = auto()
