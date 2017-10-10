import factory
from . import models


class ActiveFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Active

    name = factory.Faker('first_name')
    value = round(351200.00, 2)


class ArrearageFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Arrearage

    name = factory.Faker('first_name')
    value = round(30000, 2)


class RealEstateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RealEstate

    name = factory.Faker('first_name')
    value = round(121.21, 2)
    salable = False


class CompanyParticipationFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.CompanyParticipation

    name = factory.Faker('first_name')
    value = round(1221.21, 2)


class EquipmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Equipment

    name = factory.Faker('first_name')
    value = round(122.2, 2)


class LifeInsuranceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.LifeInsurance

    name = factory.Faker('first_name')
    value = round(121.21, 2)
    redeemable = True


class IncomeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Income

    source = factory.Faker('first_name')
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
