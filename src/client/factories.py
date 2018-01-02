import datetime
import factory.fuzzy
from lib.factories import gen_cpf
from lib.factories import gen_agency
from . import models


class ClientBaseFactory(factory.DjangoModelFactory):

    class Meta:
        abstract = True
        model = models.ClientBase
        exclude = ('now',)

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    birthday = factory.fuzzy.FuzzyNaiveDateTime(datetime.datetime(1967, 1, 1),
                                                datetime.datetime(1987, 1, 1))
    profession = factory.Faker('job')
    telephone = factory.Sequence(lambda n: '(61) 91234-5%03d' % n)
    cpf = factory.LazyAttribute(gen_cpf)
    hometown = factory.Faker('city')


class ActiveClientFactory(ClientBaseFactory):

    class Meta:
        model = models.ActiveClient

    id_document = factory.django.ImageField(color='green')
    proof_of_address = factory.django.ImageField(color='blue')

    username = factory.Faker('first_name')
    password = factory.PostGenerationMethodCall('set_password',
                                                'default123')
    email = factory.LazyAttribute(lambda x: '{}@mail.com'.format(x.username))


class ClientFactory(ClientBaseFactory):

    class Meta:
        model = models.Client

    active_spouse = factory.SubFactory(ActiveClientFactory)


class DependentFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Dependent

    active_client = factory.SubFactory(ActiveClientFactory)

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    birthday = factory.LazyFunction(datetime.datetime.now)


class BankAccountFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.BankAccount

    active_client = factory.SubFactory(ActiveClientFactory)

    agency = factory.LazyAttribute(gen_agency)
    account = factory.Sequence(lambda n: '12345-%d' % n)


class CountryFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Country

    name = factory.Faker('country')
    abbreviation = factory.Faker('country_code')


class StateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.State

    country = factory.SubFactory(CountryFactory)

    name = factory.Faker('state')
    abbreviation = factory.Faker('state_abbr')


class AddressFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Address

    active_client = factory.SubFactory(ActiveClientFactory)
    state = factory.SubFactory(StateFactory)

    city = factory.Faker('city')
    type_of_address = factory.Faker('random_letter')
    neighborhood = factory.Faker('street_name')
    detail = factory.Faker('word')
    cep = factory.Sequence(lambda n: '700000%s' % n)
    number = factory.Faker('building_number')
    complement = factory.Faker('secondary_address')
