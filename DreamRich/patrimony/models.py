from django.db import models
from django.db.models import Sum
from lib.financial_planning.flow import (
    generic_flow,
    create_array_change_annual,
)
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
import patrimony.validators as patrimony_validators
from patrimony.choices import AMORTIZATION_CHOICES


class Patrimony(models.Model):
    fgts = models.FloatField(default=0)

    def current_net_investment(self):
        total_active = self.activemanager.total
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

    def income_flow(self):
        income_changes = self.flowunitchange_set.all()
        duration = self.financialplanning.duration()
        array_change = create_array_change_annual(income_changes, duration)
        total = self.total_annual_income()
        data = generic_flow(array_change, duration, total)

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


class ActiveType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)


class ActiveManager(models.Model):

    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)
    CDI = 0.10

    @property
    def total(self):
        return self.actives.aggregate(Sum('value')).pop('value__sum', 0)

    def _update_equivalent_rate(self):
        for active in self.actives.all():
            active.update_equivalent_rate(total, self.CDI)

    @property
    def real_profit_cdi(self):
        self._update_equivalent_rate()
        total_rate = self.actives.aggregate(
                Sum('equivalent_rate')
            ).pop(
                'equivalent_rate__sum', 0
            )

        if self.CDI != 0:
            return total_rate/self.CDI
        return 0


class Active(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    equivalent_rate = models.FloatField(default=0, blank=True, null=True)

    active_type = models.ForeignKey(ActiveType,
        on_delete=models.CASCADE,
        related_name='actives')
    active_manager = models.ForeignKey(ActiveManager, 
        on_delete=models.CASCADE,
        related_name='actives')

    def _equivalent_rate_calculate(self, total, cdi):
        equivalent_rate = 0
        if total != 0:
            equivalent_rate = (self.value / total) * self.rate * cdi
        return equivalent_rate

    def update_equivalent_rate(self, total, cdi):
        new_equivalent_rate = self._equivalent_rate_calculate(total, cdi)

        percent = 0.0001  # Only update if has a change of 0.01%
        if abs(self.equivalent_rate - new_equivalent_rate) > percent:
            self.save()

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)


class Arrearage(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    period = models.PositiveIntegerField(default=0)
    rate = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(
                patrimony_validators.MIN_VALUE_RATE,
                "A taxa de juros não pode ser menor que 0%"
            ),
            MaxValueValidator(
                patrimony_validators.MAX_VALUE_RATE,
                "A taxa de juros não pode ser maior que 100%"
            )
        ]
    )
    amortization_system = models.CharField(
        max_length=5,
        choices=AMORTIZATION_CHOICES,
        default=AMORTIZATION_CHOICES[0][0]
    )
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)

class RealEstate(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    salable = models.BooleanField()
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)

class CompanyParticipation(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)

class LifeInsurance(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    redeemable = models.BooleanField()
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)

class Income(models.Model):
    source = models.CharField(max_length=100)
    value_monthly = models.FloatField(default=0)
    thirteenth = models.BooleanField()
    vacation = models.BooleanField()
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE)

    def annual(self):
        total = self.value_monthly * 12
        if self.thirteenth:
            total += self.value_monthly
        if self.vacation:
            total += self.value_monthly / 3

        return round(total, 2)

    def __str__(self):
        return "Annual({}) {}".format(self.source, self.annual())
