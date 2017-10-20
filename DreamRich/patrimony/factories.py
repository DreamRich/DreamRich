import factory
from . import models
from patrimony.choices import AMORTIZATION_CHOICES_LIST


class ActiveTypeFactory(factory.DjangoModelFactory):

    class Meta:
            model = models.ActiveType

    name = factory.Faker('word')



class ActiveFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Active

    name = factory.Faker('word')
    value = round(351200.00, 2)
    active_type = factory.SubFactory(ActiveTypeFactory)
    rate = factory.Faker('pyfloat')


class ArrearageFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Arrearage

    name = factory.Faker('word')
    value = round(30000, 2)
    period = factory.fuzzy.FuzzyInteger(50)
    rate = factory.fuzzy.FuzzyDecimal(100)
    amortization_system = factory.fuzzy.FuzzyChoice(AMORTIZATION_CHOICES_LIST)


class RealEstateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RealEstate

    name = factory.Faker('word')
    value = round(121.21, 2)
    salable = False


class CompanyParticipationFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.CompanyParticipation

    name = factory.Faker('word')
    value = round(1221.21, 2)


class EquipmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Equipment

    name = factory.Faker('word')
    value = round(122.2, 2)


class LifeInsuranceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.LifeInsurance

    name = factory.Faker('word')
    value = round(121.21, 2)
    redeemable = True


class IncomeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Income

    source = factory.Faker('word')
    value_monthly = round(51212.2, 2)
    thirteenth = True
    vacation = True


class PatrimonyMainFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Patrimony

    fgts = round(2.2, 2)
    active = factory.RelatedFactory(ActiveFactory, 'patrimony')
    arrearage = factory.RelatedFactory(ArrearageFactory, 'patrimony')
    real_estate = factory.RelatedFactory(RealEstateFactory, 'patrimony')
    company = factory.RelatedFactory(CompanyParticipationFactory, 'patrimony')
    equipment = factory.RelatedFactory(EquipmentFactory, 'patrimony')
    life_insurance = factory.RelatedFactory(LifeInsuranceFactory, 'patrimony')
    income = factory.RelatedFactory(IncomeFactory, 'patrimony')
