import datetime
import factory
from factory.fuzzy import FuzzyInteger
from financial_planning.factories import FinancialPlanningFactory
from .models import (
    GoalType,
    GoalManager,
    Goal
)


class GoalTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = GoalType

    name = factory.Sequence(lambda n: "GoalType %03d" % n)


class GoalManagerFactory(factory.DjangoModelFactory):

    financial_planning = factory.SubFactory(FinancialPlanningFactory)

    class Meta:
        model = GoalManager


class GoalFactory(factory.DjangoModelFactory):

    class Meta:
        model = Goal
        exclude = ('actual_year',)

    goal_type = factory.SubFactory(GoalTypeFactory)
    goal_manager = factory.SubFactory(GoalManagerFactory)

    has_end_date = True
    actual_year = datetime.datetime.now().year
    init_year = FuzzyInteger(actual_year, actual_year + 10)
    end_year = FuzzyInteger(actual_year + 11, actual_year + 30)
    periodicity = FuzzyInteger(1, 5)
    value = FuzzyInteger(5000, 300000)
