"""
All attributes of this file have the annual order of magnitude
"""
from django.db import models


class GoalType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class GoalManager(models.Model):

    @property
    def year_init_to_year_end(self):
        array = []
        init_year = self.financial_planning.init_year
        duration_goals = self.financial_planning.duration()
        for index in range(duration_goals):
            array.append(init_year + index)

        return array

    @property
    def goals_flow_dic(self):

        data = []
        goals = list(self.goals.all())

        for goal in goals:
            goal_flow_dic = {
                'name': goal.goal_type.name,
                'data': goal.flow,
            }
            data.append(goal_flow_dic)

        return data

    def matrix_flow_goals(self):
        matrix = []
        goals = list(self.goals.all())

        for goal in goals:
            matrix.append(goal.flow)

        return matrix

    def value_total_by_year(self):
        matrix = self.matrix_flow_goals()
        array = [sum(index) for index in zip(*matrix)]
        if not array:
            duration_goals = self.financial_planning.duration()
            array = [0] * duration_goals

        return array


class Goal(models.Model):
    has_end_date = models.BooleanField()
    init_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    periodicity = models.PositiveSmallIntegerField(null=True, blank=True)
    value = models.PositiveIntegerField()
    goal_manager = models.ForeignKey(
        GoalManager,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    goal_type = models.ForeignKey(GoalType, on_delete=models.CASCADE)

    def generic_flow_goal(self, index_goal_end):

        init_year = self.goal_manager.financial_planning.init_year
        index_goal_init = self.init_year - init_year
        mod_period = 0
        duration_goals = self.goal_manager.financial_planning.duration()
        goal_array_flow = []
        for index in range(duration_goals):
            if index > index_goal_init:
                mod_period += 1
            if index < index_goal_init:
                goal_array_flow.append(0)
            elif mod_period % self.periodicity == 0 and index <=\
                    index_goal_end:
                goal_array_flow.append(self.value)
            else:
                goal_array_flow.append(0)

        return goal_array_flow

    @property
    def flow(self):
        init_year = self.goal_manager.financial_planning.init_year
        goal_array_flow = []

        if not self.has_end_date:
            index_goal_end = self.goal_manager.financial_planning.duration()
            goal_array_flow = self.generic_flow_goal(index_goal_end)
        else:
            index_goal_end = self.end_year - init_year
            goal_array_flow = self.generic_flow_goal(index_goal_end)

        return goal_array_flow

    def total(self):
        total = sum(self.flow)

        return total

    def __str__(self):
        string_format = "Goal type = {} value = {}"
        return string_format.format(self.goal_type.name, self.value)
