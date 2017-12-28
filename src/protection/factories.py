from financial_planning.factories import FinancialPlanningFactory
from patrimony.factories import (
    ActiveManagerBaseFactory, ActiveTypeFactory,
)
from protection.models import (
    ReserveInLack, EmergencyReserve,
    ProtectionManager, PrivatePension,
    LifeInsurance, ActualPatrimonySuccession,
    IndependencePatrimonySuccession,
)
import factory


class ReserveInLackFactory(factory.DjangoModelFactory):

    class Meta:
        model = ReserveInLack

    value_0_to_24_mounth = factory.fuzzy.FuzzyInteger(0, 30000)
    value_24_to_60_mounth = factory.fuzzy.FuzzyInteger(0, 25000)
    value_60_to_120_mounth = factory.fuzzy.FuzzyInteger(0, 20000)
    value_120_to_240_mounth = factory.fuzzy.FuzzyInteger(0, 15000)


class EmergencyReserveFactory(factory.DjangoModelFactory):

    class Meta:
        model = EmergencyReserve

    mounth_of_protection = factory.fuzzy.FuzzyInteger(0, 12)


class ActualPatrimonySuccessionFactory(factory.DjangoModelFactory):

    class Meta:
        model = ActualPatrimonySuccession

    itcmd_tax = factory.Faker('pyfloat')

    oab_tax = factory.Faker('pyfloat')

    other_taxes = factory.Faker('pyfloat')


class IndependencePatrimonySuccessionFactory(factory.DjangoModelFactory):

    class Meta:
        model = IndependencePatrimonySuccession

    itcmd_tax = factory.Faker('pyfloat')

    oab_tax = factory.Faker('pyfloat')

    other_taxes = factory.Faker('pyfloat')


class PrivatePensionFactory(factory.DjangoModelFactory):

    class Meta:
        model = PrivatePension

    name = factory.Faker('word')
    annual_investment = factory.Faker('pyfloat')
    value = factory.Faker('pyfloat')
    rate = factory.Faker('pyfloat')
    active_manager = factory.SubFactory(ActiveManagerBaseFactory)
    active_type = factory.SubFactory(ActiveTypeFactory)


class LifeInsuranceFactory(factory.DjangoModelFactory):

    class Meta:
        model = LifeInsurance

    name = factory.Faker('word')
    value_to_recive = factory.Faker('pyfloat')
    value_to_pay_annual = factory.Faker('pyfloat')
    redeemable = True
    has_year_end = True
    actual = True


class ProtectionManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProtectionManager

    financial_planning = factory.SubFactory(FinancialPlanningFactory)
    reserve_in_lack = factory.RelatedFactory(ReserveInLackFactory,
                                             'protection_manager')
    actual_patrimony_protection = factory.RelatedFactory(
        ActualPatrimonySuccessionFactory,
        'protection_manager')
    future_patrimony_protection = factory.RelatedFactory(
        IndependencePatrimonySuccessionFactory,
        'protection_manager')
    private_pensions = factory.RelatedFactory(PrivatePensionFactory,
                                              'protection_manager')
    life_insurances = factory.RelatedFactory(LifeInsuranceFactory,
                                             'protection_manager')
