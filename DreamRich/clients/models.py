import datetime
from django.utils import timezone
from django.db import models

class Country(models.Model):
	country_name = models.CharField(max_length = 30)

	def __str__(self):
		return self.country_name

class State(models.Model):
	state_name = models.CharField(max_length = 30)
	country = models.ForeignKey(Country, on_delete = models.CASCADE)

class City(models.Model):
	city_name = models.CharField(max_length = 58)
	state = models.ForeignKey(State, on_delete = models.CASCADE)

class Address(models.Model):
	city = models.ForeignKey(City, on_delete = models.CASCADE)
	type_of_address = models.CharField(max_length = 10) # work or residential
	neighborhood = models.CharField(max_length = 20)
	detail = models.CharField(max_length = 50)
	number = models.IntegerField()
	complement = models.CharField(max_length = 20)

class Client(models.Model):
	name = models.CharField(max_length = 100)
	birthday = models.DateField('Data de nascimento')
	profession = models.CharField(max_length = 200)
	cpf = models.CharField(max_length = 14) # max_length considering '.' and '-'
	telephone = models.CharField(max_length = 19) # considering +55
	email = models.EmailField()
	address = models.ManyToManyField(Address)
	hometown = models.ForeignKey(City, on_delete = models.PROTECT)

	def __str__(self):
		return self.name

class Dependent(models.Model):
	client = models.ForeignKey(Client, on_delete = models.CASCADE)
	birthday = models.DateField('Data de nascimento')

class BankAccount(models.Model):
	client = models.OneToOneField(Client, on_delete = models.CASCADE) # 1-to-1
	agency = models.CharField(max_length = 6) # BR pattern: '[4alg]-[1dig]'
	account = models.CharField(max_length = 10) # BR pattern: '[8alg]-[1dig]'

	def __str__(self):
		return str(agency) + ' ' + str(account)

