import factory.fuzzy
from lib.factories import gen_cpf
from employee.models import Employee, FinancialAdviser
from dr_auth.factories import UserFactory


class EmployeeMainFactory(UserFactory):

    class Meta:
        model = Employee

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    cpf = factory.LazyAttribute(gen_cpf)


class FinancialAdviserMainFactory(EmployeeMainFactory):

    class Meta:
        model = FinancialAdviser

    @factory.post_generation
    def clients(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for client in extracted:
                self.groups.add(client)
