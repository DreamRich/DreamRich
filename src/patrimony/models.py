from django.db import models
from django.db.models import Sum
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from lib.financial_planning.flow import (
    generic_flow,
    create_array_change_annual,
)
import patrimony.validators as patrimony_validators
from patrimony.choices import AMORTIZATION_CHOICES


class Patrimony(models.Model):

    financial_planning = models.OneToOneField(
        'financial_planning.FinancialPlanning',
        on_delete=models.CASCADE,
        null=True,
        related_name='patrimony'
    )

    fgts = models.FloatField(default=0)

    def current_net_investment(self):
        total_active = self.active_manager.total()
        total_arrearage = self.arrearages.filter(period__lte=2).aggregate(
            Sum('value'))
        total = (total_active
                 - (total_arrearage['value__sum'] or 0))

        return total

    def current_property_investment(self):
        non_salable_total = self.real_estates.filter(
            salable=False).aggregate(Sum('value'))
        non_salable_total = (non_salable_total['value__sum'] or 0)

        return non_salable_total

    def possible_income_generation(self):
        total_company_participation = self.company_participations.all(
        ).aggregate(Sum('value'))
        total_equipment = self.equipments.all().aggregate(Sum('value'))
        total = (total_company_participation['value__sum'] or 0) + \
            (total_equipment['value__sum'] or 0) + self.fgts

        return total

    def total_annual_income(self):
        incomes = list(self.incomes.all())

        total = 0
        for income in incomes:
            total += income.annual()

        return total

    def income_flow(self):
        income_changes = self.flow_unit_changes.all()
        duration = self.financial_planning.duration()
        array_change = create_array_change_annual(income_changes, duration,
                                                  self.financial_planning.
                                                  init_year)
        total = self.total_annual_income()
        data = generic_flow(array_change, duration, total)

        return data

    def current_none_investment(self):
        total_movable_properties = self.movable_properties.all().aggregate(
            Sum('value'))
        total_movable_properties = (total_movable_properties['value__sum'] or 0)
        salable_total = self.real_estates.filter(
            salable=True).aggregate(Sum('value'))
        salable_total = (salable_total['value__sum'] or 0)

        total = total_movable_properties + salable_total
        return total

    def total(self):
        total = (self.current_net_investment() + self.
                 current_property_investment() + self.current_none_investment()
                 + self.possible_income_generation())

        return total


class ActiveType(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class ActiveManager(models.Model):

    patrimony = models.OneToOneField(
        'Patrimony',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='active_manager'
    )

    cdi = 0.10

    def total(self):
        return self.actives.aggregate(Sum('value')).pop('value__sum', 0)

    def _update_equivalent_rate(self):
        total = self.total()
        cdi = self.patrimony.financial_planning.cdi
        for active in self.actives.all():
            active.update_equivalent_rate(total, cdi)

    def real_profit_cdi(self):
        self._update_equivalent_rate()
        total_rate = self.actives.aggregate(
            Sum('equivalent_rate')
        ).pop(
            'equivalent_rate__sum', 0
        )
        cdi = self.patrimony.financial_planning.cdi

        if cdi != 0:
            return total_rate / cdi
        return 0

    def sum_active_same_type(self):
        data = {}
        actives_type = ActiveType.objects.all()
        for active_type in actives_type:
            actives = active_type.actives.filter(active_manager=self)
            if actives:
                data[active_type.name] = actives.aggregate(Sum('value')).\
                    pop('value__sum', 0)

    @staticmethod
    def transform_querryset_in_two_list(str_key, str_value, data):
        keys = []
        values = []
        for element in data:
            keys.append(element[str_key])
            values.append(element[str_value])

        return keys, values

    @property
    def active_type_chart(self):
        data = self.actives.order_by('active_type_id').values(
            'active_type__name').annotate(Sum('value'))
        keys, values = self.transform_querryset_in_two_list(
            'active_type__name', 'value__sum', data)
        dataset = {'labels': keys, 'data': values}
        return dataset

    @property
    def active_chart_dataset(self):
        data = self.actives.values('name', 'value').order_by('active_type_id')
        keys, values = self.transform_querryset_in_two_list(
            'value', 'name', data)
        dataset = {'labels': keys, 'data': values}
        return dataset


class Active(models.Model):

    class Meta:
        unique_together = ('name', 'active_manager', 'active_type',)

    active_type = models.ForeignKey(
        'ActiveType',
        on_delete=models.CASCADE,
        related_name='actives'
    )

    active_manager = models.ForeignKey(
        'ActiveManager',
        on_delete=models.CASCADE,
        related_name='actives'
    )

    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    equivalent_rate = models.FloatField(default=0, blank=True, null=True)

    def _equivalent_rate_calculate(self, total, cdi):
        equivalent_rate = 0
        if total != 0:
            equivalent_rate = (self.value / total) * self.rate * cdi
        return equivalent_rate

    def update_equivalent_rate(self, total, cdi):
        new_equivalent_rate = self._equivalent_rate_calculate(total, cdi)

        percent = 0.0001  # Only update if has a change of 0.01%
        if abs(self.equivalent_rate - new_equivalent_rate) > percent:
            self.equivalent_rate = new_equivalent_rate
            self.save()

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)


class ArrearageCalculator:

    def __init__(self, arrearage):
        self.calculate = arrearage
        self.outstanding_balance = self.calculate.value
        self.total_provision = 0
        self.total_interest = 0
        self.total_amortization = 0

    def calculate_arrearage(self):
        data = []
        for period in range(1, self.calculate.period + 1):
            provision = self.calculate_provision(period)
            self.total_provision += provision

            interest = self.calculate_interest(period)
            self.total_interest += interest

            amortization = self.calculate_amortization(period)
            self.total_amortization += amortization

            self.outstanding_balance -= amortization
            parameter_list = {
                'period': period,
                'provision': round(provision, 2),
                'interest': round(interest, 2),
                'amortization': round(amortization, 2),
                'outstanding_balance': round(self.outstanding_balance, 2)
            }
            data.append(parameter_list)

        data.append({
            'period': '>>',
            'provision': round(self.total_provision, 2),
            'interest': round(self.total_interest, 2),
            'amortization': round(self.total_amortization, 2),
            'outstanding_balance': '<< TOTAIS'
        })
        return data

    def calculate_interest(self, period):
        interest = 0

        value = self.calculate.value
        calculated_period = self.calculate.period
        rate = self.calculate.rate

        if (self.calculate.amortization_system == AMORTIZATION_CHOICES[0][0] or
                self.calculate.rate == 0):
            interest = ((
                value - (
                    (period - 1) * value / calculated_period
                )
            ) * (rate / 100))
        elif self.calculate.amortization_system == AMORTIZATION_CHOICES[1][0]:
            provision = self.calculate_provision(period)
            amortization = self.calculate_amortization(period)
            interest = provision - amortization
        else:
            interest = 0

        return interest

    def calculate_amortization(self, period):
        amortization = 0

        if (self.calculate.amortization_system == AMORTIZATION_CHOICES[0][0] or
                self.calculate.rate == 0):
            amortization = self.calculate.value / self.calculate.period
        elif self.calculate.amortization_system == AMORTIZATION_CHOICES[1][0]:
            first_amortization = (
                self.calculate_provision(1) -
                (self.calculate.value * (self.calculate.rate / 100))
            )
            amortization = first_amortization * \
                ((1 + (self.calculate.rate / 100))**(period - 1))
        else:
            amortization = self.calculate.value / self.calculate.period

        return amortization

    def calculate_provision(self, period):
        provision = 0

        rate = self.calculate.rate
        value = self.calculate.value
        calculated_period = self.calculate.period

        if (self.calculate.amortization_system == AMORTIZATION_CHOICES[0][0] or
                self.calculate.rate == 0):
            amortization = self.calculate_amortization(period)
            interest = self.calculate_interest(period)
            provision = amortization + interest
        elif self.calculate.amortization_system == AMORTIZATION_CHOICES[1][0]:
            provision = (
                value * (rate / 100) /
                (1 - (1 + (rate / 100))**(-calculated_period))
            )
        else:
            provision = self.calculate.value / self.calculate.period

        return provision


class Arrearage(models.Model):

    patrimony = models.ForeignKey(
        'Patrimony',
        on_delete=models.CASCADE,
        related_name='arrearages'
    )

    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    actual_period = models.PositiveIntegerField(default=0)
    period = models.PositiveIntegerField(default=1)
    rate = models.FloatField(
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
    )

    @property
    def calculate_arrearage(self):
        arrearage_calculator = ArrearageCalculator(self)
        return arrearage_calculator.calculate_arrearage

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)


class RealState(models.Model):

    patrimony = models.ForeignKey(
        'Patrimony',
        on_delete=models.CASCADE,
        related_name='real_estates'
    )

    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    salable = models.BooleanField()

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)


class CompanyParticipation(models.Model):

    patrimony = models.ForeignKey(
        'Patrimony',
        on_delete=models.CASCADE,
        related_name='company_participations'
    )

    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)


class MovableProperty(models.Model):

    patrimony = models.ForeignKey(
        'Patrimony',
        on_delete=models.CASCADE,
        related_name='movable_properties'
    )

    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)


class Equipment(models.Model):

    patrimony = models.ForeignKey(
        'Patrimony',
        on_delete=models.CASCADE,
        related_name='equipments'
    )

    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)

    def __str__(self):
        return "{name} {value}".format(**self.__dict__)


class Income(models.Model):

    patrimony = models.ForeignKey(
        'Patrimony',
        on_delete=models.CASCADE,
        related_name='incomes'
    )

    source = models.CharField(max_length=100)
    value_monthly = models.FloatField(default=0)
    thirteenth = models.BooleanField(default=False)
    fourteenth = models.BooleanField(default=False)
    vacation = models.BooleanField(default=False)

    def annual(self):
        total = self.value_monthly * 12
        if self.thirteenth:
            total += self.value_monthly
        if self.vacation:
            total += self.value_monthly / 3

        return round(total, 2)

    def __str__(self):
        return "Annual({}) {}".format(self.source, self.annual())
