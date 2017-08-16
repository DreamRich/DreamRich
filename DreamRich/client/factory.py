import datetime
import factory.fuzzy
import random

from . import models

class CountryFactory(factory.Factory):
	class Meta:
		model = models.Country

	name = factory.Sequence(lambda n: 'country%s' % n)

class StateFactory(factory.Factory):
	class Meta:
		model = models.State

	name = factory.Sequence(lambda n: 'state%s' % n)

class CityFactory(factory.Factory):
	class Meta:
		model = models.City

	name = factory.Sequence(lambda n: 'city%s' % n)

class AddressFactory(factory.Factory):
	class Meta:
		model = models.Address

	city = factory.SubFactory(CityFactory)
	type_of_address = factory.Sequence(lambda n: 'type%s' % n)
	neighborhood = factory.Sequence(lambda n: 'neighborhood%s' % n)
	detail = factory.Sequence(lambda n: 'detail%s' % n)
	number = 1
	complement = factory.Sequence(lambda n: 'complement%s' % n)

class ClientFactory(factory.Factory):
	class Meta:
		model = models.Client

	name = factory.Faker('name')
	birthday = factory.LazyFunction(datetime.datetime.now)
	profession = factory.Sequence(lambda n: 'profession%s' % n)
	cpf = factory.Sequence(lambda n: '%s' % n)
	telephone = factory.Sequence(lambda n: 'tel%s' % n)
	email = factory.Sequence(lambda n: '%s@gmail.com' % n)
	address = factory.SubFactory(AddressFactory)
	hometown = factory.SubFactory(CityFactory)

class Dependent(factory.Factory):
	class Meta:
		model = models.Dependent

	client = factory.SubFactory(ClientFactory)
	birthday = factory.LazyFunction(datetime.datetime.now)

class BankAccount(factory.Factory):
	class Meta:
		model = models.BankAccount

	client = factory.RelatedFactory(ClientFactory)
	agency = factory.Sequence(lambda n: '%s' % n)
	account = factory.Sequence(lambda n: '%s' % n)


