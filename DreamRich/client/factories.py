import datetime
import factory.fuzzy
import random

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
	id_document = factory.django.ImageField(color='green')
	proof_of_address = factory.django.ImageField(color='blue')
	birthday = factory.LazyFunction(datetime.datetime.now)
	profession = factory.Sequence(lambda n: 'profession%s' % n)
	telephone = factory.Sequence(lambda n: 'tel%s' % n)
	email = factory.Sequence(lambda n: '%s@gmail.com' % n)
	hometown = factory.SubFactory(CityFactory)
	cpf = '775.214.611-00'

	@factory.post_generation
	def addresses(self, create, extracted, **kwargs):
		if not create:
			# Simple build, do nothing.
			return

		if extracted:
			# A list of groups were passed in, use them
			for address in extracted:
				self.addresses.add(address)

class Dependent(factory.DjangoModelFactory):
	class Meta:
		model = models.Dependent

	client = factory.SubFactory(ClientFactory)
	birthday = factory.LazyFunction(datetime.datetime.now)

class BankAccount(factory.DjangoModelFactory):
	class Meta:
		model = models.BankAccount

	client = factory.RelatedFactory(ClientFactory)
	agency = factory.Sequence(lambda n: '%s' % n)
	account = factory.Sequence(lambda n: '%s' % n)


