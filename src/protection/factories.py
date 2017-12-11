from patrimony.factories import PatrimonyMainFactory
from financial_planning.factories import FinancialPlanningFactory
from protection.models import (
    ReserveInLack,
    EmergencyReserve,
    ProtectionManager,
    PrivatePension,
    LifeInsurance,
    ActualPatrimonyProtection,
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


class PrivatePensionFactory(factory.DjangoModelFactory):

    class Meta:
        model = PrivatePension

    name = factory.Faker('word')
    value_annual = factory.Faker('pyfloat')
    accumulated = factory.Faker('pyfloat')


class ProtectionManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProtectionManager

    financial_planning = factory.SubFactory(FinancialPlanningFactory)


class ActualPatrimonyProtectionFactory(factory.DjangoModelFactory):

    class Meta:
        model = ActualPatrimonyProtection

    itcmd_tax = factory.Faker('pyfloat')

    oab_tax = factory.Faker('pyfloat')

    other_taxes = factory.Faker('pyfloat')

    patrimony = factory.SubFactory(PatrimonyMainFactory)

    reserve_in_lack = factory.SubFactory(ReserveInLackFactory)

    private_pension = factory.RelatedFactory(PrivatePensionFactory,
                                             'actual_patrimony_protection')


class LifeInsuranceFactory(factory.DjangoModelFactory):

    class Meta:
        model = LifeInsurance

    name = factory.Faker('word')
    value_to_recive = factory.Faker('pyfloat')
    value_to_pay_annual = factory.Faker('pyfloat')
    redeemable = True
    has_year_end = True
    actual = True
    protection_manager = factory.SubFactory(ProtectionManagerFactory)
    actual_patrimony_protection = factory.SubFactory(
                                    ActualPatrimonyProtectionFactory)
