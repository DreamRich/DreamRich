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
    target_profitability = 110


class RegularCostFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RegularCost

    home = round(12.2, 2)
    electricity_bill = round(12.2, 2)
    gym = round(12.2, 2)
    taxes = round(12.2, 2)
    car_gas = round(12.2, 2)
    insurance = round(12.2, 2)
    cellphone = round(12.2, 2)
    health_insurance = round(12.2, 2)
    supermarket = round(12.2, 2)
    housekeeper = round(12.2, 2)
    beauty = round(12.2, 2)
    internet = round(12.2, 2)
    netflix = round(12.2, 2)
    recreation = round(12.2, 2)
    meals = round(12.2, 2)
    appointments = round(12.2, 2)
    drugstore = round(12.2, 2)
    extras = round(12.2, 2)


class FinancialPlanningFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialPlanning

    active_client = factory.SubFactory(ActiveClientMainFactory)
    patrimony = factory.SubFactory(PatrimonyMainFactory)
    financial_independence = factory.SubFactory(FinancialIndependenceFactory)
    goal_manager = factory.SubFactory(GoalManagerFactory)
    regular_cost = factory.SubFactory(RegularCostFactory)
    cdi = round(0.1213, 4)
    ipca = round(0.075, 4)


class GoalMainFactory():

    @staticmethod
    def create():

        financial_planning = FinancialPlanningFactory()
        goal_manager = financial_planning.goal_manager
        GoalFactory.create_batch(8, goal_manager=goal_manager)
