"""
All attributes of this file have the annual order of magnitude
"""
from django.db import models
import datetime


class GoalType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GoalManager(models.Model):

    @property
    def year_init_to_year_end(self):
        array = []
        actual_year = datetime.datetime.now().year
        duration_goals = self.financialplanning.duration()
        for index in range(duration_goals):
            array.append(actual_year + index)

        return array

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

    def matrix_flow_goals(self):
        matrix = []
        goals = list(self.goal_set.all())

        for goal in goals:
            matrix.append(goal.flow)

        return matrix

    def value_total_by_year(self):
        matrix = self.matrix_flow_goals()

        array = [sum(index) for index in zip(*matrix)]

        return array


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
        duration_goals = self.goal_manager.financialplanning.duration()
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
            index_goal_end = self.goal_manager.financialplanning.duration()
            goal_array_flow = self.generic_flow(index_goal_end, actual_year)
        else:
            index_goal_end = self.year_end - actual_year
            goal_array_flow = self.generic_flow(index_goal_end, actual_year)

        return goal_array_flow

    def __str__(self):
        string_format = "Goal type = {} value = {}"
        return string_format.format(self.goal_type.name,self.value)
