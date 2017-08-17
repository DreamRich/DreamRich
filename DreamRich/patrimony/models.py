from django.db import models
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When


class Patrimony(models.Model):
    fgts = models.DecimalField(decimal_places = 2, max_digits = 8)

    @property
    def current_net_investment(self):
        total_active = self.active_set.all().aggregate(Sum('value'))
        total_arrearage = self.arrearage_set.all().aggregate(Sum('value'))
        total = total_active['value__sum'] - total_arrearage['value__sum']

        return total

    @property
    def current_property_investment(self):
        salable_total = self.realestate_set.filter(salable=True).aggregate(Sum('value'))
        salable_total = salable_total['value__sum']

        return salable_total

    @property
    def possible_income_generation(self):
        total_company_participation = self.companyparticipation_set.all().aggregate(Sum('value'))
        total_equipment = self.equipment_set.all().aggregate(Sum('value'))
        total = total_company_participation['value__sum'] + total_equipment['value__sum'] + self.fgts

        return total

    @property
    def current_monthly_income(self):
        total_value_monthly = self.income_set.all().aggregate(Sum('value_monthly'))
        total_value_monthly = total_value_monthly['value_monthly__sum']
        total_vacation = self.income_set.all().aggregate(Sum('vacation'))
        total_vacation = total_vacation['vacation__sum']
        total_thirteenth = self.income_set.all().aggregate(Sum('thirteenth'))
        total_thirteenth = total_thirteenth['thirteenth__sum']
        total_vacation_monthly = total_vacation / 12
        total_thirteenth_monthly = total_thirteenth / 12

        total = total_value_monthly + total_vacation_monthly + total_thirteenth_monthly
        total = round(total,2)

        return total

class Active(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

class Arrearage(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

class RealEstate(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8)
    salable = models.BooleanField()
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

class CompanyParticipation(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

class Equipment(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

class LifeInsurance(models.Model):
    name = models.CharField(max_length = 100)
    value = models.DecimalField(decimal_places = 2, max_digits = 8)
    redeemable = models.BooleanField()
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

class Income(models.Model):
    source = models.CharField(max_length = 100)
    value_monthly = models.DecimalField(decimal_places = 2, max_digits = 8)
    thirteenth = models.DecimalField(decimal_places = 2, max_digits = 8)
    vacation = models.DecimalField(decimal_places = 2, max_digits = 8)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

class Leftover(models.Model):
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

    @property
    def leftover(self):
        self.patrimony.current_monthly_income - self.patrimony.regularcost.total

class RegularCost(models.Model):
    patrimony = models.OneToOneField(Patrimony, on_delete = models.CASCADE, primary_key=True)

    home = models.DecimalField(decimal_places = 2, max_digits = 8)
    electricity_bill = models.DecimalField(decimal_places = 2, max_digits = 8)
    gym = models.DecimalField(decimal_places = 2, max_digits = 8)
    taxes = models.DecimalField(decimal_places = 2, max_digits = 8)
    car_gas = models.DecimalField(decimal_places = 2, max_digits = 8)
    insurance = models.DecimalField(decimal_places = 2, max_digits = 8)
    cellphone = models.DecimalField(decimal_places = 2, max_digits = 8)
    health_insurance = models.DecimalField(decimal_places = 2, max_digits = 8)
    supermarket = models.DecimalField(decimal_places = 2, max_digits = 8)
    housekeeper = models.DecimalField(decimal_places = 2, max_digits = 8)
    beauty = models.DecimalField(decimal_places = 2, max_digits = 8)
    internet = models.DecimalField(decimal_places = 2, max_digits = 8)
    netflix = models.DecimalField(decimal_places = 2, max_digits = 8)
    recreation = models.DecimalField(decimal_places = 2, max_digits = 8)
    meals = models.DecimalField(decimal_places = 2, max_digits = 8)
    appointments = models.DecimalField(decimal_places = 2, max_digits = 8) # consultas
    drugstore = models.DecimalField(decimal_places = 2, max_digits = 8)
    extras = models.DecimalField(decimal_places = 2, max_digits = 8)

    @property
    def total(self):
        total_regular_cost = self.home + self.electricity_bill + self.gym + self.taxes \
        + self.car_gas + self.insurance + self.cellphone + self.health_insurance \
        + self.supermarket + self.housekeeper + self.beauty + self.internet \
        + self.netflix + self.recreation + self.meals + self.appointments \
        + self.drugstore + self.extras

        return total_regular_cost
