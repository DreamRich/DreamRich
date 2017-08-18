import datetime
import factory.fuzzy
import random
from client.validators import validate_CPF
from faker import Factory

from . import models
fake = Factory.create('pt_BR')


def gen_cpf(factory):
    cpf = ""
    while cpf == "":
        try:
            cpf = validate_CPF(fake.cpf())
        except:
            pass
    return cpf

    
class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Country

    name = factory.Sequence(lambda n: 'country%s' % n)

class StateFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.State

    name = factory.Sequence(lambda n: 'state%s' % n)
    country = factory.SubFactory(CountryFactory)

class CityFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.City

    name = factory.Sequence(lambda n: 'city%s' % n)
    state = factory.SubFactory(StateFactory)

class AddressFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Address

    city = factory.SubFactory(CityFactory)
    type_of_address = factory.Sequence(lambda n: 'type%s' % n)
    neighborhood = factory.Sequence(lambda n: 'neighborhood%s' % n)
    detail = factory.Sequence(lambda n: 'detail%s' % n)
    number = 1
    complement = factory.Sequence(lambda n: 'complement%s' % n)

class ClientFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Client

    name = factory.Faker('name')
    surname = factory.Faker('name')
    birthday = factory.LazyFunction(datetime.datetime.now)
    profession = factory.Sequence(lambda n: 'profession%s' % n)
    telephone = factory.Sequence(lambda n: 'tel%s' % n)
    email = factory.Sequence(lambda n: '%s@gmail.com' % n)
    hometown = factory.SubFactory(CityFactory)
    cpf = factory.LazyAttribute(gen_cpf)

    @factory.post_generation
    def addresses(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for address in extracted:
                self.addresses.add(address)

class DependentFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Dependent

    name = factory.Faker('name')
    surname = factory.Faker('name')
    birthday = factory.LazyFunction(datetime.datetime.now)

class BankAccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.BankAccount

    agency = factory.Sequence(lambda n: '%s' % n)
    account = factory.Sequence(lambda n: '%s' % n)

class ActiveClientFactory(ClientFactory):

    class Meta:
        model = models.ActiveClient

    id_document = factory.django.ImageField(color='green')
    proof_of_address = factory.django.ImageField(color='blue')
    spouse = factory.SubFactory(ClientFactory)
    bank_account = factory.RelatedFactory(BankAccountFactory, "active_client")
    dependent = factory.RelatedFactory(DependentFactory, "active_client")    




