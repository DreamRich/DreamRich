import factory
from client.factories import ActiveClientMainFactory
from patrimony.factories import PatrimonyMainFactory
from goal.factories import GoalManagerFactory, GoalFactory
from protection.factories import ProtectionManagerFactory
from . import models


class FinancialIndependenceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialIndependence

    age = 60
    duration_of_usufruct = 20
    remain_patrimony = 200000


class CostTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.CostType

    name = factory.Sequence(lambda n: "RegularCost %03d" % n)


class RegularCostFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RegularCost

    value = factory.Faker('pyint')
    cost_type = factory.SubFactory(CostTypeFactory)


class CostManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.CostManager

    @factory.post_generation
    def _regular_cost(self, create, *unused_args, **unused_kwargs):
        if create:
            return RegularCostFactory.create_batch(18,
                                                   cost_manager=self,
                                                   value=round(12.2, 2))

        return RegularCostFactory.build_batch(18, value=round(12.2, 2))


class FinancialPlanningFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialPlanning

    active_client = factory.SubFactory(ActiveClientMainFactory)
    patrimony = factory.SubFactory(PatrimonyMainFactory)
    financial_independence = factory.SubFactory(FinancialIndependenceFactory)
    goal_manager = factory.SubFactory(GoalManagerFactory)
    cost_manager = factory.SubFactory(CostManagerFactory)
    protection_manager = factory.SubFactory(ProtectionManagerFactory)
    target_profitability = 110
    cdi = round(0.1213, 4)
    ipca = round(0.075, 4)


class GoalMainFactory():

    @staticmethod
    def create():
        financial_planning = FinancialPlanningFactory()
        goal_manager = financial_planning.goal_manager
        GoalFactory.create_batch(8, goal_manager=goal_manager)
