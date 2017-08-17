import factory
from decimal import Decimal
from . import models


class ActiveFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Active

    name = factory.Faker('first_name')
    value = round(Decimal(1.1),2)

class ArrearageFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Arrearage

    name = factory.Faker('first_name')
    value = round(Decimal(0.2),2)

class RealEstateFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.RealEstate

    name = factory.Faker('first_name')
    value = round(Decimal(121.21),2)
    salable = True

class CompanyParticipationFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.CompanyParticipation

    name = factory.Faker('first_name')
    value = round(Decimal(1221.21),2)

class EquipmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Equipment

    name = factory.Faker('first_name')
    value = round(Decimal(122.2),2)

class LifeInsuranceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.LifeInsurance

    name = factory.Faker('first_name')
    value = round(Decimal(121.21),2)
    redeemable = True

class IncomeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Income

    source = factory.Faker('first_name')
    value_monthly = round(Decimal(1212.2),2)
    thirteenth = round(Decimal(1212.2),2)
    vacation = round(Decimal(1212.2),2)

class LeftoverFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Leftover

class RegularCostFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.RegularCost

    home = round(Decimal(12.2),2)
    electricity_bill = round(Decimal(12.2),2)
    gym = round(Decimal(12.2),2)
    taxes = round(Decimal(12.2),2)
    car_gas = round(Decimal(12.2),2)
    insurance = round(Decimal(12.2),2)
    cellphone = round(Decimal(12.2),2)
    health_insurance = round(Decimal(12.2),2)
    supermarket = round(Decimal(12.2),2)
    housekeeper = round(Decimal(12.2),2)
    beauty = round(Decimal(12.2),2)
    internet = round(Decimal(12.2),2)
    netflix = round(Decimal(12.2),2)
    recreation = round(Decimal(12.2),2)
    meals = round(Decimal(12.2),2)
    appointments = round(Decimal(12.2),2)
    drugstore = round(Decimal(12.2),2)
    extras = round(Decimal(12.2),2)

class PatrimonyFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Patrimony

    fgts = round(Decimal(2.2),2)
    active = factory.RelatedFactory(ActiveFactory, 'patrimony')
    arrearage = factory.RelatedFactory(ArrearageFactory, 'patrimony')
    real_estate = factory.RelatedFactory(RealEstateFactory, 'patrimony')
    company = factory.RelatedFactory(CompanyParticipationFactory, 'patrimony')
    equipment = factory.RelatedFactory(EquipmentFactory, 'patrimony')
    life_insurance = factory.RelatedFactory(LifeInsuranceFactory, 'patrimony')
    income = factory.RelatedFactory(IncomeFactory, 'patrimony')
    leftover = factory.RelatedFactory(LeftoverFactory, 'patrimony')
    regular_cost = factory.RelatedFactory(RegularCostFactory, 'patrimony')
