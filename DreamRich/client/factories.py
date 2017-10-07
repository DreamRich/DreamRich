import datetime
import factory.fuzzy
from lib.factories import gen_cpf
from lib.factories import gen_agency
from . import models


class CountryFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Country

    name = factory.Sequence(lambda n: 'country%s' % n)
    abbreviation = factory.Sequence(lambda n: '%2d' % (n %1000))


class StateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.State

    name = factory.Sequence(lambda n: 'state%s' % n)
    abbreviation = factory.Sequence(lambda n: '%s' % (n%100))
    country = factory.SubFactory(CountryFactory)


class AddressFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Address

    city = factory.Faker('word')
    type_of_address = factory.Sequence(lambda n: 'type%s' % n)
    neighborhood = factory.Sequence(lambda n: 'neighborhood%s' % n)
    detail = factory.Sequence(lambda n: 'detail%s' % n)
    cep = factory.Sequence(lambda n: '700000%s' % n)
    state = factory.SubFactory(StateFactory)
    number = factory.Faker('pyint')
    complement = factory.Sequence(lambda n: 'complement%s' % n)


class ClientFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Client
        exclude = ('now',)

    name = factory.Faker('name')
    surname = factory.Faker('name')
    birthday = factory.fuzzy.FuzzyNaiveDateTime(datetime.datetime(1967, 1, 1),
                                                datetime.datetime(1987, 1, 1))
    profession = factory.Sequence(lambda n: 'profession%s' % n)
    telephone = factory.Sequence(lambda n: '(61) 91234-56%02d' % n)
    hometown = factory.Faker('word')
    cpf = factory.LazyAttribute(gen_cpf)


class DependentFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Dependent

    name = factory.Faker('name')
    surname = factory.Faker('name')
    birthday = factory.LazyFunction(datetime.datetime.now)


class BankAccountFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.BankAccount

    agency = factory.LazyAttribute(gen_agency)
    account = factory.Sequence(lambda n: '12345-%d' % n)


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
    address = factory.RelatedFactory(AddressFactory, 'active_client')
    dependent = factory.RelatedFactory(DependentFactory, "active_client")
