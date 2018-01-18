import factory
from financial_planning.factories import FinancialPlanningFactory
from . import models
from .choices import AMORTIZATION_CHOICES_LIST


class PatrimonyFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Patrimony

    financial_planning = factory.SubFactory(
        FinancialPlanningFactory
    )

    fgts = round(2.2, 2)


class ActiveTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.ActiveType

    name = factory.Sequence(lambda n: "ActiveType %03d" % n)


class ActiveManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.ActiveManager

    patrimony = factory.SubFactory(PatrimonyFactory)


class ActiveFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Active

    active_type = factory.SubFactory(ActiveTypeFactory)
    active_manager = factory.SubFactory(ActiveManagerFactory)

    name = factory.Sequence(lambda n: "Active %03d" % n)
    value = round(351200.00, 2)
    rate = factory.Faker('pyfloat')
    equivalent_rate = factory.Faker('pyfloat')


class ArrearageFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Arrearage

    patrimony = factory.SubFactory(PatrimonyFactory)

    name = factory.Faker('word')
    value = round(30000, 2)
    period = 2
    rate = factory.fuzzy.FuzzyDecimal(100)
    amortization_system = factory.fuzzy.FuzzyChoice(AMORTIZATION_CHOICES_LIST)


class RealEstateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RealEstate

    patrimony = factory.SubFactory(PatrimonyFactory)

    name = factory.Faker('word')
    value = round(121.21, 2)
    salable = False


class CompanyParticipationFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.CompanyParticipation

    patrimony = factory.SubFactory(PatrimonyFactory)

    name = factory.Faker('word')
    value = round(1221.21, 2)


class MovablePropertyFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.MovableProperty

    patrimony = factory.SubFactory(PatrimonyFactory)

    name = factory.Faker('word')
    value = round(121.21, 2)


class EquipmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Equipment

    patrimony = factory.SubFactory(PatrimonyFactory)

    name = factory.Faker('word')
    value = round(122.2, 2)


class IncomeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Income

    patrimony = factory.SubFactory(PatrimonyFactory)

    source = factory.Faker('word')
    value_monthly = round(51212.2, 2)
    thirteenth = True
    vacation = True


class ActiveManagerBaseFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.ActiveManager

    patrimony = factory.SubFactory(PatrimonyFactory)
