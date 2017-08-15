import factory
from . import models

class PatrimonyFactory(factory.Factory):
    class Meta:
        model = models.Patrimony

    fgts = 2.2

class ActiveFactory(factory.Factory):
    class Meta:
        model = models.Active

    name = factory.Faker('first_name')
    value = 1.1
    patrimony = factory.SubFactory(PatrimonyFactory)
