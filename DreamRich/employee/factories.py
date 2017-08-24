import datetime
import factory.fuzzy
from django.contrib.auth.models import User
from lib.factories import gen_cpf
from faker import Factory
from employee.models import Employee, FinancialAdviser


class EmployeeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Employee

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    cpf = factory.LazyAttribute(gen_cpf)
    username = factory.Faker('word')

class FinancialAdviserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = FinancialAdviser

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    cpf = factory.LazyAttribute(gen_cpf)
    username = factory.Faker('word')

    @factory.post_generation
    def clients(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for client in extracted:
                self.groups.add(client)
