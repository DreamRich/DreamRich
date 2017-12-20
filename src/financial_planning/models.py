import datetime
import numpy
from django.core.exceptions import ValidationError
from django.db import models
from dreamrich import models as base_models
from client.models import ActiveClient
from patrimony.models import Patrimony
from goal.models import GoalManager, GoalType
from lib.financial_planning.flow import (
    generic_flow,
    create_array_change_annual,
)
from lib.profit.profit import actual_rate


class FinancialIndependence(models.Model):
    age = models.PositiveSmallIntegerField()
    duration_of_usufruct = models.PositiveSmallIntegerField()
    remain_patrimony = models.PositiveIntegerField()
    rate = models.FloatField()

    def assets_required(self):
        rate = self.financial_planning.real_gain()

        return numpy.pv(rate, self.duration_of_usufruct,
                        -self.remain_patrimony * 12)

    def remain_necessary_for_retirement(self):
        assets_required = -self.assets_required()
        rate_target_profitability = self.financial_planning. \
            real_gain_related_cdi()
        years_for_retirement = self.financial_planning.duration()
        current_net_investment = self.financial_planning.patrimony.\
            current_net_investment()
        total = numpy.pmt(rate_target_profitability, years_for_retirement,
                          current_net_investment, assets_required)
        total /= 12
        if total < 0:
            total = 0

        return total

    # Will be considerate only goals that represent properties and equity
    # interests
    def filter_goals_that_will_be_monetized(self):

        goal_manager = self.financial_planning.goal_manager
        type_home = GoalType.objects.filter(name='Moradia').first()
        type_society_participation = GoalType.objects.filter(
            name='Compra De Cotas Societárias').first()
        type_extra_home = GoalType.objects.filter(name='Casa Extra').first()
        type_house_reform = GoalType.objects.filter(
            name='Reforma e Manutenção Da Casa').first()

        goals = goal_manager.goals.filter(
            models.Q(
                goal_type=type_home) | models.Q(
                goal_type=type_society_participation) | models.Q(
                goal_type=type_extra_home) | models.Q(
                    goal_type=type_house_reform))
        return list(goals)

    def patrimony_at_end(self):
        actual_patrimony = self.financial_planning.patrimony.total()
        patrimony_in_independence = self.financial_planning.\
            suggested_flow_patrimony['flow'][-1]
        goals_monetized = self.goals_monetized()
        total = actual_patrimony + patrimony_in_independence +\
            goals_monetized

        return total

    def goals_monetized(self):
        goals = self.filter_goals_that_will_be_monetized()
        total = 0

        for goal in goals:
            year_monitized = self.financial_planning.end_year() - goal.end_year
            final_rate = (1 + self.rate) ** year_monitized
            total += goal.total() * final_rate

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
        duration = self.financial_planning.duration()
        array_change = create_array_change_annual(cost_changes, duration,
                                                  self.financial_planning.
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


class FlowUnitChange(base_models.BaseModel):

    annual_value = models.FloatField()

    year = models.PositiveSmallIntegerField()

    cost_manager = models.ForeignKey(CostManager, on_delete=models.CASCADE,
                                     null=True, blank=True)

    incomes = models.ForeignKey(Patrimony, on_delete=models.CASCADE,
                                null=True, blank=True)

    def clean(self):
        # Don't allow cost_manager and incomes id's null together
        if self.cost_manager is None and self.incomes is None:
            raise ValidationError("cost_manager_id and incomes_id can't be" +
                                  " null together. Instaciate one")

        # Don't allow cost_manager and incomes instaciate together
        if self.cost_manager is not None and self.incomes is not None:
            raise ValidationError("cost_manager_id and incomes_id can't be" +
                                  " instanciate together. Instaciate just one")


class FinancialPlanning(models.Model):

    active_client = models.OneToOneField(
        ActiveClient,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='financial_planning'
    )

    patrimony = models.OneToOneField(
        Patrimony,
        on_delete=models.CASCADE,
        null=True,
        related_name='financial_planning'
    )

    financial_independence = models.OneToOneField(
        FinancialIndependence,
        on_delete=models.CASCADE,
        null=True,
        related_name='financial_planning'
    )

    goal_manager = models.OneToOneField(
        GoalManager,
        on_delete=models.CASCADE,
        null=True,
        related_name='financial_planning'
    )

    cost_manager = models.OneToOneField(
        CostManager,
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

    def is_complete(self):
        fields = ['cost_manager', 'goal_manager', 'financial_independence',
                  'patrimony']

        for field in fields:
            if not hasattr(
                self,
                field) or (
                hasattr(
                    self,
                    field) and getattr(
                    self,
                    field +
                    '_id') is None):
                return False

        return True

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

    def generic_annual_leftovers(self, remain_necessary_for_retirement,
                                 spent_with_annual_protection):
        income_flow = self.patrimony.income_flow()
        regular_cost_flow = self.cost_manager.flow()
        goal_value_total_by_year = self.goal_manager.value_total_by_year()

        data = []

        for index in range(self.duration()):
            actual_leftovers_for_goals = income_flow[index] -\
                goal_value_total_by_year[index] -\
                regular_cost_flow[index] -\
                remain_necessary_for_retirement -\
                spent_with_annual_protection[index]

            data.append(actual_leftovers_for_goals)

        return data

    def annual_leftovers_for_goal(self):

        remain_necessary_for_retirement = self.financial_independence.\
            remain_necessary_for_retirement()
        spent_with_annual_protection = self.protection_manager.flow()

        data = self.generic_annual_leftovers(remain_necessary_for_retirement,
                                             spent_with_annual_protection)

        return data

    def annual_leftovers(self):
        duration = self.duration()
        array_zero = [0] * duration
        data = self.generic_annual_leftovers(0, array_zero)

        return data

    def real_gain_related_cdi(self):
        return actual_rate(self.target_profitability / 100 * self.cdi,
                           self.ipca)

    def resource_monetization(self, flow, rate):
        total_goals = self.goal_manager.value_total_by_year()
        duration = self.duration()

        resource = [0] * (duration)
        resource[0] = flow[0]

        for index in range(duration - 1):
            leftover_this_year = resource[index] - total_goals[index]
            resource_monetized = leftover_this_year * rate
            resource[index + 1] = flow[index] + resource_monetized

        return resource

    @property
    def year_init_to_end(self):
        init_year = self.init_year
        duration_goals = self.duration()
        range_year = range(init_year, init_year + duration_goals)
        array = list(range_year)
        return array

    @property
    def total_resource_for_annual_goals(self):
        annual_leftovers_for_goal = self.annual_leftovers_for_goal()
        rate = self.real_gain_related_cdi() + 1
        resource_for_goal = self.resource_monetization(
            annual_leftovers_for_goal, rate)

        return resource_for_goal

    @property
    def suggested_flow_patrimony(self):
        annual_leftovers = self.annual_leftovers()
        rate = self.real_gain_related_cdi() + 1
        flow = self.resource_monetization(annual_leftovers, rate)

        return {'flow': flow, 'rate': rate}

    @property
    def actual_flow_patrimony(self):
        annual_leftovers = self.annual_leftovers()
        real_gain = self.patrimony.activemanager.real_profit_cdi()
        flow = self.resource_monetization(annual_leftovers, real_gain)

        return {'flow': flow, 'rate': real_gain}
