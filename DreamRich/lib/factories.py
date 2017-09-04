from faker import Factory
from dreamrich.validators import validate_cpf

fake = Factory.create('pt_BR')


def gen_cpf(factory):
    cpf = ""
    while cpf == "":
        try:
            cpf = validate_cpf(fake.cpf())
        except BaseException:
            pass

    return cpf
