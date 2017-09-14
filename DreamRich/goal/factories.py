import factory
from . import models

class FinancialIndependenceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialIndependence

    age = 60
    duration_of_usufruct = 20
    remain_patrimony = 200000


class GoalTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.GoalType


    name = factory.Faker('word')


class GoalFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Goal


    is_periodic = True
    year_init = 2018
    year_end = 2040
    periodicity = 1
    value = 22000
    financial_independence = factory.SubFactory(FinancialIndependenceFactory)
    goal_type = factory.SubFactory(GoalTypeFactory)


class MainFactory():

    @staticmethod
    def create():
        financial_independence = FinancialIndependenceFactory()
        GoalFactory.create_batch(
                5,
                financial_independence=financial_independence,
                )
