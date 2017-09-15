import factory
from . import models
from financial_planning.factories  import FinancialPlanningFactory


class FinancialIndependenceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialIndependence

    age = 60
    duration_of_usufruct = 20
    remain_patrimony = 200000
    financial_planning = factory.SubFactory(FinancialPlanningFactory)


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
    goal_type = factory.SubFactory(GoalTypeFactory)
    financial_planning = factory.SubFactory(FinancialPlanningFactory)
