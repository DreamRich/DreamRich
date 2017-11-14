import datetime
import numpy
from django.db import models
from client.models import ActiveClient
from patrimony.models import Patrimony
from goal.models import GoalManager
from lib.financial_planning.flow import (
    generic_flow,
    create_array_change_annual,
)
from lib.profit.profit import actual_rate
from protection.models import ProtectionManager


class FinancialIndependence(models.Model):
    age = models.PositiveSmallIntegerField()
    duration_of_usufruct = models.PositiveSmallIntegerField()
    remain_patrimony = models.PositiveIntegerField()

    def assets_required(self):
        rate = self.financialplanning.real_gain()

        return numpy.pv(rate, self.duration_of_usufruct,
                        -self.remain_patrimony * 12)

    def remain_necessary_for_retirement(self):
        assets_required = -self.assets_required()
        rate_dic = self.financialplanning.real_gain_related_cdi()
        target_profitability = self.financialplanning.target_profitability
        rate_target_profitability = rate_dic[target_profitability]
        years_for_retirement = self.financialplanning.duration()
        current_net_investment = self.financialplanning.patrimony.\
            current_net_investment()
        total = numpy.pmt(rate_target_profitability, years_for_retirement,
                          current_net_investment, assets_required)
        total /= 12
        if total < 0:
            total = 0

        return total


class CostType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CostManager(models.Model):

    def total(self):
        total_query = self.regular_costs.aggregate(models.Sum('value'))
        total = total_query.pop('value__sum', 0)
        return total

    @property
    def total_cost(self):
        return self.total()

    def flow(self):
        cost_changes = self.flowunitchange_set.all()
        duration = self.financialplanning.duration()
        array_change = create_array_change_annual(cost_changes, duration,
                                                  self.financialplanning.
                                                  init_year)
        total_annual = self.total() * 12
        data = generic_flow(array_change, duration, total_annual)

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


class FlowUnitChange(models.Model):

    annual_value = models.FloatField()

    year = models.PositiveSmallIntegerField()

    cost_manager = models.ForeignKey(CostManager, on_delete=models.CASCADE,
                                     null=True)

    incomes = models.ForeignKey(Patrimony, on_delete=models.CASCADE,
                                null=True)


class FinancialPlanning(models.Model):

    active_client = models.OneToOneField(
        ActiveClient,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    patrimony = models.OneToOneField(
        Patrimony,
        on_delete=models.CASCADE,
        null=True,
    )

    financial_independence = models.OneToOneField(
        FinancialIndependence,
        on_delete=models.CASCADE,
        null=True,
    )

    goal_manager = models.OneToOneField(
        GoalManager,
        on_delete=models.CASCADE,
        null=True,
    )

    cost_manager = models.OneToOneField(
        CostManager,
        on_delete=models.CASCADE,
        null=True,
    )

    protection_manager = models.OneToOneField(
        ProtectionManager,
        on_delete=models.CASCADE,
        null=True,
        related_name='financial_planning'
    )

    init_year = models.PositiveSmallIntegerField(null=True)

    cdi = models.FloatField()

    ipca = models.FloatField()

    target_profitability = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if not self.init_year:
            self.init_year = datetime.datetime.now().year

        super(FinancialPlanning, self).save(*args, **kwargs)

    def end_year(self):
        age_of_independence = self.financial_independence.age
        actual_year = datetime.datetime.now().year
        birthday_year = self.active_client.birthday.year
        actual_age = actual_year - birthday_year
        end_year = age_of_independence - actual_age + actual_year

        return end_year

    def duration(self):
        duration = self.end_year() - self.init_year

        return duration

    def real_gain(self):
        return actual_rate(self.cdi, self.ipca)

    def annual_leftovers_for_goal(self):

        income_flow = self.patrimony.income_flow()
        regular_cost_flow = self.cost_manager.flow()
        goal_value_total_by_year = self.goal_manager.value_total_by_year()
        remain_necessary_for_retirement = self.financial_independence.\
            remain_necessary_for_retirement()
        spent_with_annual_protection = 2000

        data = []

        for index in range(self.duration()):
            actual_leftovers_for_goals = income_flow[index] -\
                goal_value_total_by_year[index] -\
                regular_cost_flow[index] -\
                remain_necessary_for_retirement -\
                spent_with_annual_protection

            data.append(actual_leftovers_for_goals)

        return data

    def real_gain_related_cdi(self):
        cdi_initial = 80
        cdi_final = 205
        data = {}
        for rate in range(cdi_initial, cdi_final, 5):
            cdi_rate = actual_rate(rate / 100 * self.cdi, self.ipca)
            data[rate] = cdi_rate
        return data

    @property
    def total_resource_for_annual_goals(self):

        annual_leftovers_for_goal = self.annual_leftovers_for_goal()
        total_goals = self.goal_manager.value_total_by_year()
        duration = self.duration()

        resource_for_goal = [0] * (duration)
        resource_for_goal[0] = annual_leftovers_for_goal[0]
        rate_dic = self.real_gain_related_cdi()
        real_gain = rate_dic[self.target_profitability] + 1

        for index in range(duration - 1):
            leftover_this_year = resource_for_goal[index] - total_goals[index]
            resource_for_goal_monetized = leftover_this_year * real_gain
            resource_for_goal[index + 1] = annual_leftovers_for_goal[index] +\
                resource_for_goal_monetized

        return resource_for_goal
