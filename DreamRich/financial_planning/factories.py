import factory
from . import models
from client.factories import ActiveClientMainFactory
from patrimony.factories import PatrimonyMainFactory
from goal.factories import GoalManagerFactory


class FinancialIndependenceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialIndependence

    age = 60
    duration_of_usufruct = 20
    remain_patrimony = 200000


class FinancialPlanningFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialPlanning

    active_client = factory.SubFactory(ActiveClientMainFactory)
    patrimony = factory.SubFactory(PatrimonyMainFactory)
    financial_independence = factory.SubFactory(FinancialIndependenceFactory)
    goal_manager = factory.SubFactory(GoalManagerFactory)
