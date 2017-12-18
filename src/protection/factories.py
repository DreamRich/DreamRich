from protection.models import (
    ReserveInLack,
    EmergencyReserve,
    ProtectionManager,
    PrivatePension,
    LifeInsurance,
)
import factory


class ReserveInLackFactory(factory.DjangoModelFactory):

    class Meta:
        model = ReserveInLack

    value_0_to_24_month = factory.fuzzy.FuzzyInteger(0, 30000)
    value_24_to_60_month = factory.fuzzy.FuzzyInteger(0, 25000)
    value_60_to_120_month = factory.fuzzy.FuzzyInteger(0, 20000)
    value_120_to_240_month = factory.fuzzy.FuzzyInteger(0, 15000)


class EmergencyReserveFactory(factory.DjangoModelFactory):

    class Meta:
        model = EmergencyReserve

    month_of_protection = factory.fuzzy.FuzzyInteger(0, 12)


class PrivatePensionFactory(factory.DjangoModelFactory):

    class Meta:
        model = PrivatePension

    name = factory.Faker('word')
    value_annual = factory.Faker('pyfloat')
    accumulated = factory.Faker('pyfloat')


class LifeInsuranceFactory(factory.DjangoModelFactory):

    class Meta:
        model = LifeInsurance

    name = factory.Faker('word')
    value_to_recive = factory.Faker('pyfloat')
    value_to_pay_annual = factory.Faker('pyfloat')
    redeemable = True
    has_year_end = True


class ProtectionManagerFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProtectionManager

    reserve_in_lack = factory.SubFactory(ReserveInLackFactory)

    emergency_reserve = factory.SubFactory(EmergencyReserveFactory)

    private_pension = factory.RelatedFactory(PrivatePensionFactory,
                                             'protection_manager')

    life_insurance = factory.RelatedFactory(LifeInsuranceFactory,
                                            'protection_manager')
