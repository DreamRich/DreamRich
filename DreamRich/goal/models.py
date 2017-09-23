"""
All attributes of this file have the annual order of magnitude
"""
from django.db import models
import datetime


class GoalType(models.Model):
    name = models.CharField(max_length=100)


class GoalManager(models.Model):

    @property
    def duration_goals(self):
        age_of_independence = self.financialplanning.financial_independence.age
        actual_year = datetime.datetime.now().year
        birthday_year = self.financialplanning.active_client.birthday.year
        actual_age = actual_year - birthday_year
        duration_goals = age_of_independence - actual_age

        return duration_goals

    @property
    def goals_flow_dic(self):

        data = []
        goals = list(self.goal_set.all())

        for goal in goals:
            goal_flow_dic = {
                'name': goal.goal_type.name,
                'data': goal.flow,
            }
            data.append(goal_flow_dic)

        return data


class Goal(models.Model):
    has_end_date = models.BooleanField()
    year_init = models.PositiveSmallIntegerField()
    year_end = models.PositiveSmallIntegerField(null=True, blank=True)
    periodicity = models.PositiveSmallIntegerField()
    value = models.PositiveIntegerField()
    goal_manager = models.ForeignKey(
        GoalManager,
        on_delete=models.CASCADE
    )
    goal_type = models.ForeignKey(GoalType, on_delete=models.CASCADE)

    def generic_flow(self, index_goal_end, actual_year):

        index_goal_init = self.year_init - actual_year
        mod_period = 0
        duration_goals = self.goal_manager.duration_goals
        goal_array_flow = []
        for index in range(duration_goals):
            if index > index_goal_init:
                mod_period += 1
            if index < index_goal_init:
                goal_array_flow.append(0)
            elif mod_period % self.periodicity == 0 and index < index_goal_end:
                goal_array_flow.append(self.value)
            else:
                goal_array_flow.append(0)

        return goal_array_flow

    @property
    def flow(self):
        actual_year = datetime.datetime.now().year
        goal_array_flow = []
        index_goal_end = self.year_end - actual_year

        if not self.has_end_date:
            index_goal_end = self.goal_manager.duration_goals
            goal_array_flow = self.generic_flow(index_goal_end, actual_year)
        else:
            index_goal_end = self.year_end - actual_year
            goal_array_flow = self.generic_flow(index_goal_end, actual_year)

        return goal_array_flow
