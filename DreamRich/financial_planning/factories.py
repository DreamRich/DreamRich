import factory
from . import models
from client.factories import (
    ActiveClientMainFactory,
)



class FinancialPlanningFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FinancialPlanning

    active_client = factory.SubFactory(ActiveClientMainFactory)
