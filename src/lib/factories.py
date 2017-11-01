import functools
import random
from faker import Factory
from dreamrich.validators import validate_cpf

FAKE_GENERATOR = Factory.create('pt_BR')


def gen_cpf(unused_factory):
    cpf = ""
    while cpf == "":
        try:
            cpf = validate_cpf(
                FAKE_GENERATOR.cpf()  # pylint: disable=no-member
            )
        except BaseException:
            pass

    return cpf


def gen_agency(unused_factory):
    while True:
        try:
            number = functools.partial(random.randint, 0, 9)
            agency = "{}{}{}{}-{}".format(number(), number(),
                                          number(), number(), number()
                                          )
            return agency
        except BaseException:
            pass
