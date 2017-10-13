from django.db import models
from client.models import ActiveClient
from patrimony.models import Patrimony
from goal.models import GoalManager
from lib.financial_planning.flow import generic_flow
from lib.profit.profit import actual_rate
import datetime
import numpy


class FinancialIndependence(models.Model):
    age = models.PositiveSmallIntegerField()
    duration_of_usufruct = models.PositiveSmallIntegerField()
    remain_patrimony = models.PositiveIntegerField()

    def assets_required(self):
        rate = float(self.financialplanning.real_gain())

        return numpy.pv(rate, self.duration_of_usufruct,
                        -self.remain_patrimony * 12)

    def remain_necessary_for_retirement(self):
        assets_required = -self.assets_required()
        rate = 0.0544
        years_for_retirement = self.financialplanning.duration()
        current_net_investment = float(self.financialplanning.patrimony.
                                       current_net_investment())
        total = numpy.pmt(rate, years_for_retirement, current_net_investment,
                          assets_required)
        total /= 12
        if total < 0:
            total = 0

        return total


class CostType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CostManager(models.Model):

#    home = models.FloatField(default=0)
#    electricity_bill = models.FloatField(default=0)
#    gym = models.FloatField(default=0)
#    taxes = models.FloatField(default=0)
#    car_gas = models.FloatField(default=0)
#    insurance = models.FloatField(default=0)
#    cellphone = models.FloatField(default=0)
#    health_insurance = models.FloatField(default=0)
#    supermarket = models.FloatField(default=0)
#    housekeeper = models.FloatField(default=0)
#    beauty = models.FloatField(default=0)
#    internet = models.FloatField(default=0)
#    netflix = models.FloatField(default=0)
#    recreation = models.FloatField(default=0)
#    meals = models.FloatField(default=0)
#    appointments = models.FloatField(default=0)  # consultas
#    drugstore = models.FloatField(default=0)
#    extras = models.FloatField(default=0)

    def total(self):
        total_query = self.regular_costs.aggregate(models.Sum('value'))
        total = total_query.pop('value__sum', 0)
        return total

    @property
    def total_cost(self):
        return self.total()

    def flow(self, regular_cost_change):
        duration = self.financialplanning.duration()
        total = self.total()
        data = generic_flow(regular_cost_change, duration, total)

        return data


class RegularCost(models.Model):

    value = models.FloatField(default=0)
    cost_type = models.ForeignKey(CostType, on_delete=models.CASCADE)
    cost_manager = models.ForeignKey(
        CostManager,
        related_name='regular_costs',
        on_delete=models.CASCADE
    )

    def __str__(self):
        if self.cost_type_id is not None:
            return '{} {}'.format(self.cost_type.name, self.value)
        return str(self.value)


class FinancialPlanning(models.Model):

    active_client = models.OneToOneField(
        ActiveClient,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    patrimony = models.OneToOneField(
        Patrimony,
        on_delete=models.CASCADE,
    )

    financial_independence = models.OneToOneField(
        FinancialIndependence,
        on_delete=models.CASCADE,
    )

    goal_manager = models.OneToOneField(
        GoalManager,
        on_delete=models.CASCADE,
    )

    cost_manager = models.OneToOneField(
        CostManager,
        on_delete=models.CASCADE
    )

    cdi = models.FloatField()

    ipca = models.FloatField()

    def duration(self):
        age_of_independence = self.financial_independence.age
        actual_year = datetime.datetime.now().year
        birthday_year = self.active_client.birthday.year
        actual_age = actual_year - birthday_year
        duration = age_of_independence - actual_age

        return duration

    def real_gain(self):
        return actual_rate(self.cdi, self.ipca)

    def change_flow(self):
        data = []
        for index in range(self.duration()):
            data.append(0)

        return data

    def annual_leftovers_for_objectives(self):
        change = self.change_flow()
        goal_value_total_by_year = self.goal_manager.value_total_by_year()
        income_flow = self.patrimony.income_flow(change)
        regular_cost_flow = self.cost_manager.flow(change)
        remain_necessary_for_retirement = self.financial_independence.\
            remain_necessary_for_retirement()
        spent_with_annual_protection = 2000

        data = []

        for index in range(self.duration()):
            actual_leftovers_for_objectives = income_flow[index] -\
                goal_value_total_by_year[index] -\
                regular_cost_flow[index] -\
                remain_necessary_for_retirement -\
                spent_with_annual_protection

            data.append(actual_leftovers_for_objectives)

        return data
