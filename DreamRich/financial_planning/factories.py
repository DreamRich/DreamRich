import factory
from . import models
from client.factories import ActiveClientMainFactory
from patrimony.factories import PatrimonyMainFactory
from goal.factories import GoalManagerFactory, GoalFactory
from decimal import Decimal


class FinancialIndependenceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialIndependence

    age = 60
    duration_of_usufruct = 20
    remain_patrimony = 200000


class RegularCostFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RegularCost

    home = round(Decimal(12.2), 2)
    electricity_bill = round(Decimal(12.2), 2)
    gym = round(Decimal(12.2), 2)
    taxes = round(Decimal(12.2), 2)
    car_gas = round(Decimal(12.2), 2)
    insurance = round(Decimal(12.2), 2)
    cellphone = round(Decimal(12.2), 2)
    health_insurance = round(Decimal(12.2), 2)
    supermarket = round(Decimal(12.2), 2)
    housekeeper = round(Decimal(12.2), 2)
    beauty = round(Decimal(12.2), 2)
    internet = round(Decimal(12.2), 2)
    netflix = round(Decimal(12.2), 2)
    recreation = round(Decimal(12.2), 2)
    meals = round(Decimal(12.2), 2)
    appointments = round(Decimal(12.2), 2)
    drugstore = round(Decimal(12.2), 2)
    extras = round(Decimal(12.2), 2)


class FinancialPlanningFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialPlanning

    active_client = factory.SubFactory(ActiveClientMainFactory)
    patrimony = factory.SubFactory(PatrimonyMainFactory)
    financial_independence = factory.SubFactory(FinancialIndependenceFactory)
    goal_manager = factory.SubFactory(GoalManagerFactory)
    regular_cost = factory.SubFactory(RegularCostFactory)
    cdi = round(Decimal(12.13), 2)
    ipca = round(Decimal(7.5), 2)


class GoalMainFactory():

    @staticmethod
    def create():

        financial_planning = FinancialPlanningFactory()
        goal_manager = financial_planning.goal_manager
        GoalFactory.create_batch(8, goal_manager=goal_manager)
