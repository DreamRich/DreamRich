from django.db import models
from django.db.models import Sum
from lib.financial_planning.flow import generic_flow


class Patrimony(models.Model):
    fgts = models.DecimalField(decimal_places=2, max_digits=8)

    def current_net_investment(self):
        total_active = self.active_set.all().aggregate(Sum('value'))
        total_arrearage = self.arrearage_set.all().aggregate(Sum('value'))
        total = ((total_active['value__sum'] or 0)
                 - (total_arrearage['value__sum'] or 0))

        return total

    def current_property_investment(self):
        non_salable_total = self.realestate_set.filter(
            salable=False).aggregate(Sum('value'))
        non_salable_total = (non_salable_total['value__sum'] or 0)

        return non_salable_total

    def possible_income_generation(self):
        total_company_participation = self.companyparticipation_set.all(
        ).aggregate(Sum('value'))
        total_equipment = self.equipment_set.all().aggregate(Sum('value'))
        total = (total_company_participation['value__sum'] or 0) + \
            (total_equipment['value__sum'] or 0) + self.fgts

        return total

    def total_annual_income(self):
        total = 0
        incomes = list(self.income_set.all())

        for income in incomes:
            total += income.annual()

        return total

    def income_flow(self, income_change):
        duration = self.financialplanning.duration()
        total = self.total_annual_income()
        data = generic_flow(income_change, duration, total)

        return data

    def current_none_investment(self):
        total_movable_property = self.movableproperty_set.all().aggregate(
            Sum('value'))
        total_movable_property = (total_movable_property['value__sum'] or 0)
        salable_total = self.realestate_set.filter(
            salable=True).aggregate(Sum('value'))
        salable_total = (salable_total['value__sum'] or 0)

        total = total_movable_property + salable_total
        return total


class Active(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)


class Arrearage(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)


class RealEstate(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    salable = models.BooleanField()
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)


class CompanyParticipation(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)


class LifeInsurance(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    redeemable = models.BooleanField()
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)


class Income(models.Model):
    source = models.CharField(max_length=100)
    value_monthly = models.DecimalField(decimal_places=2, max_digits=8,
                                        default=0)
    thirteenth = models.BooleanField()
    vacation = models.BooleanField()
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

    def annual(self):
        total = self.value_monthly*12
        if self.thirteenth:
            total += self.value_monthly
        if self.vacation:
            total += self.value_monthly/3

        return round(total,2)

    def __str__(self):
        return "Annual {}".format(self.annual())
