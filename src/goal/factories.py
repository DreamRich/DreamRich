import datetime
import factory
from factory.fuzzy import FuzzyInteger
from . import models


class GoalTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.GoalType

    name = factory.Sequence(lambda n: "GoalType %03d" % n)


class GoalManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.GoalManager


class GoalFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Goal
        exclude = ('actual_year',)

    has_end_date = True
    actual_year = datetime.datetime.now().year
    year_init = FuzzyInteger(actual_year, actual_year + 10)
    year_end = FuzzyInteger(actual_year + 11, actual_year + 30)
    periodicity = FuzzyInteger(1, 5)
    value = FuzzyInteger(5000, 300000)
    goal_type = factory.SubFactory(GoalTypeFactory)
    goal_manager = factory.SubFactory(GoalManagerFactory)
