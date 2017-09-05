import datetime
import factory.fuzzy
from lib.factories import gen_cpf
from . import models


class CountryFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Country

    name = factory.Sequence(lambda n: 'country%s' % n)


class StateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.State

    name = factory.Sequence(lambda n: 'state%s' % n)
    country = factory.SubFactory(CountryFactory)


class AddressFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Address

    city = factory.Faker('word')
    type_of_address = factory.Sequence(lambda n: 'type%s' % n)
    neighborhood = factory.Sequence(lambda n: 'neighborhood%s' % n)
    detail = factory.Sequence(lambda n: 'detail%s' % n)
    state = factory.SubFactory(StateFactory)
    number = 1
    complement = factory.Sequence(lambda n: 'complement%s' % n)


class ClientFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Client

    name = factory.Faker('name')
    surname = factory.Faker('name')
    birthday = factory.LazyFunction(datetime.datetime.now)
    profession = factory.Sequence(lambda n: 'profession%s' % n)
    telephone = factory.Sequence(lambda n: '1234467%s' % n)
    hometown = factory.Faker('word')
    cpf = factory.LazyAttribute(gen_cpf)
    address = factory.RelatedFactory(AddressFactory)

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


class ActiveClientMainFactory(ClientFactory):

    class Meta:
        model = models.ActiveClient

    id_document = factory.django.ImageField(color='green')
    proof_of_address = factory.django.ImageField(color='blue')
    client_bank_account = factory.RelatedFactory(BankAccountFactory,
                                                 'active_client')

    username = factory.Faker('word')
    password = factory.PostGenerationMethodCall('set_password',
                                                'default123')
    email = factory.LazyAttribute(lambda x: '{}@mail.com'.format(x.username))

    spouse = factory.RelatedFactory(ClientFactory, 'active_spouse')
    dependent = factory.RelatedFactory(DependentFactory, "active_client")
