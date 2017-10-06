from django.db import models
from client.models import ActiveClient
from patrimony.models import Patrimony
from goal.models import GoalManager
from lib.financial_planning.flow import generic_flow
from lib.profit.profit import actual_rate
from decimal import Decimal
import datetime
import numpy


class FinancialIndependence(models.Model):
    age = models.PositiveSmallIntegerField()
    duration_of_usufruct = models.PositiveSmallIntegerField()
    remain_patrimony = models.PositiveIntegerField()
    target_profitability = models.PositiveIntegerField()

    def assets_required(self):
        rate = float(self.financialplanning.real_gain())

        return numpy.pv(rate, self.duration_of_usufruct,
                        -self.remain_patrimony * 12)

    def remain_necessary_for_retirement(self):
        assets_required = -self.assets_required()
        rate = self.financialplanning.real_gain_related_cdi()
        rate_target_profitability = float(rate[self.target_profitability])
        years_for_retirement = self.financialplanning.duration()
        current_net_investment = float(self.financialplanning.patrimony.\
                                       current_net_investment())
        total = numpy.pmt(rate_target_profitability, years_for_retirement,\
                          current_net_investment, assets_required)
        total /= 12
        if total < 0:
            total = 0

        return total


class RegularCost(models.Model):

    home = models.FloatField(default=0)
    electricity_bill = models.FloatField(default=0)
    gym = models.FloatField(default=0)
    taxes = models.FloatField(default=0)
    car_gas = models.FloatField(default=0)
    insurance = models.FloatField(default=0)
    cellphone = models.FloatField(default=0)
    health_insurance = models.FloatField(default=0)
    supermarket = models.FloatField(default=0)
    housekeeper = models.FloatField(default=0)
    beauty = models.FloatField(default=0)
    internet = models.FloatField(default=0)
    netflix = models.FloatField(default=0)
    recreation = models.FloatField(default=0)
    meals = models.FloatField(default=0)
    appointments = models.FloatField(default=0)  # consultas
    drugstore = models.FloatField(default=0)
    extras = models.FloatField(default=0)

    def total(self):
        total = self.home + self.electricity_bill + self.gym + self.taxes \
            + self.car_gas + self.insurance + self.cellphone \
            + self.health_insurance + self.supermarket + self.housekeeper \
            + self.beauty + self.internet + self.netflix + self.recreation \
            + self.meals + self.appointments + self.drugstore + self.extras

        return total

    def flow(self, regular_cost_change):
        duration = self.financialplanning.duration()
        total = self.total()
        data = generic_flow(regular_cost_change, duration, total)

        return data


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

    regular_cost = models.OneToOneField(
        RegularCost,
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
        regular_cost_flow = self.regular_cost.flow(change)
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

    def real_gain_related_cdi(self):
        real_gain_cdi = {rate: actual_rate(Decimal(rate/100) * self.cdi, self.ipca) for rate in range(80, 205, 5)}
        return real_gain_cdi;


