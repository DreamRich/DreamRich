import factory
from client.factories import ActiveClientFactory
from . import models


class FinancialPlanningFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.FinancialPlanning

    active_client = factory.SubFactory(ActiveClientFactory)

    cdi = round(0.1213, 4)
    ipca = round(0.075, 4)
    target_profitability = 1.10


class FinancialIndependenceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialIndependence

    financial_planning = factory.SubFactory(FinancialPlanningFactory)

    age = 60
    duration_of_usufruct = 20
    remain_patrimony = 200000
    rate = factory.Faker('pyfloat')


class CostTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.CostType

    name = factory.Sequence(lambda n: "RegularCost %03d" % n)


class CostManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.CostManager

    financial_planning = factory.SubFactory(FinancialPlanningFactory)

    @factory.post_generation
    def _regular_cost(self, create, *unused_args, **unused_kwargs):
        predicted_regular_types = 18

        if create:
            return RegularCostFactory.create_batch(predicted_regular_types,
                                                   cost_manager=self,
                                                   value=round(12.2, 2))

        return RegularCostFactory.build_batch(predicted_regular_types,
                                              cost_manager=self,
                                              value=round(12.2, 2))


class RegularCostFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RegularCost

    cost_manager = factory.SubFactory(CostManagerFactory)
    cost_type = factory.SubFactory(CostTypeFactory)

    value = factory.Faker('pyint')
