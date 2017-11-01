import datetime
import factory.fuzzy
from lib.factories import gen_cpf
from lib.factories import gen_agency
from . import models


class CountryFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Country

    name = factory.Faker('country')
    abbreviation = factory.Faker('country_code')


class StateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.State

    name = factory.Faker('state')
    abbreviation = factory.Faker('state_abbr')
    country = factory.SubFactory(CountryFactory)


class AddressFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Address

    city = factory.Faker('city')
    type_of_address = factory.Faker('random_letter')
    neighborhood = factory.Faker('street_name')
    detail = factory.Faker('word')
    cep = factory.Sequence(lambda n: '700000%s' % n)
    state = factory.SubFactory(StateFactory)
    number = factory.Faker('building_number')
    complement = factory.Faker('secondary_address')


class ClientFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Client
        exclude = ('now',)

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    birthday = factory.fuzzy.FuzzyNaiveDateTime(datetime.datetime(1967, 1, 1),
                                                datetime.datetime(1987, 1, 1))
    profession = factory.Faker('job')
    telephone = factory.Sequence(lambda n: '(61) 91234-56%02d' % n)
    hometown = factory.Faker('city')
    cpf = factory.LazyAttribute(gen_cpf)


class DependentFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Dependent

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
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

    username = factory.Faker('first_name')
    password = factory.PostGenerationMethodCall('set_password',
                                                'default123')
    email = factory.LazyAttribute(lambda x: '{}@mail.com'.format(x.username))

    spouse = factory.RelatedFactory(ClientFactory, 'active_spouse')
    address = factory.RelatedFactory(AddressFactory, 'active_client')
    dependent = factory.RelatedFactory(DependentFactory, "active_client")
