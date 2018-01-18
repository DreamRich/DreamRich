import factory.fuzzy
from lib.factories import gen_cpf
from employee.models import Employee, FinancialAdviser
from dr_auth.factories import UserFactory


class EmployeeFactory(UserFactory):

    class Meta:
        model = Employee

    cpf = factory.LazyAttribute(gen_cpf)


class FinancialAdviserFactory(EmployeeFactory):

    class Meta:
        model = FinancialAdviser

    @factory.post_generation
    def clients(self, create, extracted):
        if not create:
            return

        if extracted:
            for client in extracted:
                self.groups.add(client)
