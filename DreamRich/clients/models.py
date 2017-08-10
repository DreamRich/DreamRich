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

class RegularCosts(models.Model):
	client = models.ForeignKey(Client, on_delete = models.CASCADE)

	home = models.DecimalField(decimal_places = 2, max_digits = 8)
	electricity_bill = models.DecimalField(decimal_places = 2, max_digits = 8)
	gym = models.DecimalField(decimal_places = 2, max_digits = 8)
	taxes = models.DecimalField(decimal_places = 2, max_digits = 8)
	car_gas = models.DecimalField(decimal_places = 2, max_digits = 8)
	insurance = models.DecimalField(decimal_places = 2, max_digits = 8)
	cellphone = models.DecimalField(decimal_places = 2, max_digits = 8)
	health_insurance = models.DecimalField(decimal_places = 2, max_digits = 8)
	supermarket = models.DecimalField(decimal_places = 2, max_digits = 8)
	housekeeper = models.DecimalField(decimal_places = 2, max_digits = 8)
	beauty = models.DecimalField(decimal_places = 2, max_digits = 8)
	internet = models.DecimalField(decimal_places = 2, max_digits = 8)
	netflix = models.DecimalField(decimal_places = 2, max_digits = 8)
	recreation = models.DecimalField(decimal_places = 2, max_digits = 8)
	meals = models.DecimalField(decimal_places = 2, max_digits = 8)
	appointments = models.DecimalField(decimal_places = 2, max_digits = 8) # consultas
	drugstore = models.DecimalField(decimal_places = 2, max_digits = 8)
	extras = models.DecimalField(decimal_places = 2, max_digits = 8)


class Dependent(models.Model):
	client = models.ForeignKey(Client, on_delete = models.CASCADE)
	birthday = models.DateField('Data de nascimento')

class BankAccount(models.Model):
	client = models.OneToOneField(Client, on_delete = models.CASCADE) # 1-to-1
	agency = models.CharField(max_length = 6) # BR pattern: '[4alg]-[1dig]'
	account = models.CharField(max_length = 10) # BR pattern: '[8alg]-[1dig]'

	def __str__(self):
		return str(agency) + ' ' + str(account)


