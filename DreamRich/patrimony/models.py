from django.db import models
from django.db.models import Sum


class Patrimony(models.Model):
    fgts = models.DecimalField(decimal_places=2, max_digits=8)

    @property
    def current_net_investment(self):
        total_active = self.active_set.all().aggregate(Sum('value'))
        total_arrearage = self.arrearage_set.all().aggregate(Sum('value'))
        total = ((total_active['value__sum'] or 0)
                 - (total_arrearage['value__sum'] or 0))

        return total

    @property
    def current_property_investment(self):
        non_salable_total = self.realestate_set.filter(
            salable=False).aggregate(Sum('value'))
        non_salable_total = (non_salable_total['value__sum'] or 0)

        return non_salable_total

    @property
    def possible_income_generation(self):
        total_company_participation = self.companyparticipation_set.all(
        ).aggregate(Sum('value'))
        total_equipment = self.equipment_set.all().aggregate(Sum('value'))
        total = (total_company_participation['value__sum'] or 0) + \
            (total_equipment['value__sum'] or 0) + self.fgts

        return total

    @property
    def current_monthly_income(self):
        total_value_monthly = self.income_set.all().aggregate(
            Sum('value_monthly'))
        total_value_monthly = total_value_monthly['value_monthly__sum']
        total_vacation = self.income_set.all().aggregate(Sum('vacation'))
        total_vacation = total_vacation['vacation__sum']
        total_thirteenth = self.income_set.all().aggregate(Sum('thirteenth'))
        total_thirteenth = total_thirteenth['thirteenth__sum']
        total_vacation_monthly = total_vacation / 12
        total_thirteenth_monthly = total_thirteenth / 12

        total = total_value_monthly + total_vacation_monthly \
                                    + total_thirteenth_monthly
        total = round(total, 2)

        return total

    @property
    def current_none_investment(self):
        total_movable_property = self.movableproperty_set.all().aggregate(
            Sum('value'))
        total_movable_property = (total_movable_property['value__sum'] or 0)
        salable_total = self.realestate_set.filter(
            salable=True).aggregate(Sum('value'))
        salable_total = (salable_total['value__sum'] or 0)

        total = total_movable_property + salable_total
        return total

    @property
    def leftover(self):
        return (self.current_monthly_income - self.regularcost.total)


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
    thirteenth = models.DecimalField(decimal_places=2, max_digits=8)
    vacation = models.DecimalField(decimal_places=2, max_digits=8)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)
