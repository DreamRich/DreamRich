import factory
from . import models
from client.factories import ActiveClientMainFactory
from patrimony.factories import PatrimonyMainFactory
from goal.factories import GoalManagerFactory, GoalFactory


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


class GoalMainFactory():

    @staticmethod
    def create():

        financial_planning = FinancialPlanningFactory()
        goal_manager = financial_planning.goal_manager
        GoalFactory.create_batch(8,goal_manager = goal_manager)
