import factory
from . import models


class GoalTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.GoalType

    name = factory.Faker('word')


class GoalManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.GoalManager


class GoalFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Goal

    is_periodic = True
    year_init = 2018
    year_end = 2040
    periodicity = 1
    value = 22000
    goal_type = factory.SubFactory(GoalTypeFactory)
