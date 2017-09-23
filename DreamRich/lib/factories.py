from faker import Factory
from dreamrich.validators import validate_cpf
import functools
import random

fake = Factory.create('pt_BR')


def gen_cpf(factory):
    cpf = ""
    while cpf == "":
        try:
            cpf = validate_cpf(fake.cpf())
        except BaseException:
            pass

    return cpf


def gen_agency(factory):
    while True:
        try:
            number = functools.partial(random.randint, 0, 9)
            gen = lambda: "{}{}{}{}-{}".format(number(), number(), number(),
                                               number(), number())
            agency = gen()
            return agency
        except BaseException:
            pass
