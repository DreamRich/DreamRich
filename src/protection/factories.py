import factory
from patrimony.factories import (
    ActiveFactory,
    PatrimonyFactory
)
from protection.models import (
    ReserveInLack, EmergencyReserve,
    ProtectionManager, PrivatePension,
    LifeInsurance, ActualPatrimonySuccession,
    IndependencePatrimonySuccession,
)
from financial_planning.factories import (
    FinancialPlanningFactory,
    CostManagerFactory
)


class EmergencyReserveFactory(factory.DjangoModelFactory):

    class Meta:
        model = EmergencyReserve

    patrimony = factory.SubFactory(PatrimonyFactory)
    cost_manager = factory.SubFactory(CostManagerFactory)

    month_of_protection = factory.fuzzy.FuzzyInteger(0, 12)


class ProtectionManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProtectionManager

    financial_planning = factory.SubFactory(FinancialPlanningFactory)


class ReserveInLackFactory(factory.DjangoModelFactory):

    class Meta:
        model = ReserveInLack

    protection_manager = factory.SubFactory(ProtectionManagerFactory)

    value_0_to_24_month = factory.fuzzy.FuzzyInteger(0, 30000)
    value_24_to_60_month = factory.fuzzy.FuzzyInteger(0, 25000)
    value_60_to_120_month = factory.fuzzy.FuzzyInteger(0, 20000)
    value_120_to_240_month = factory.fuzzy.FuzzyInteger(0, 15000)


class ActualPatrimonySuccessionFactory(factory.DjangoModelFactory):

    class Meta:
        model = ActualPatrimonySuccession

    protection_manager = factory.SubFactory(ProtectionManagerFactory)
    reserve_in_lack = factory.SubFactory(ReserveInLackFactory)

    itcmd_tax = factory.Faker('pyfloat')
    oab_tax = factory.Faker('pyfloat')
    other_taxes = factory.Faker('pyfloat')


class IndependencePatrimonySuccessionFactory(factory.DjangoModelFactory):

    class Meta:
        model = IndependencePatrimonySuccession

    protection_manager = factory.SubFactory(ProtectionManagerFactory)
    reserve_in_lack = factory.SubFactory(ReserveInLackFactory)

    itcmd_tax = factory.Faker('pyfloat')
    oab_tax = factory.Faker('pyfloat')
    other_taxes = factory.Faker('pyfloat')


class PrivatePensionFactory(ActiveFactory):

    class Meta:
        model = PrivatePension

    protection_manager = factory.SubFactory(ProtectionManager)

    annual_investment = factory.Faker('pyfloat')


class LifeInsuranceFactory(factory.DjangoModelFactory):

    class Meta:
        model = LifeInsurance

    protection_manager = factory.SubFactory(ProtectionManager)

    name = factory.Faker('word')
    value_to_recive = factory.Faker('pyfloat')
    value_to_pay_annual = factory.Faker('pyfloat')
    redeemable = True
    has_year_end = True
    actual = True
