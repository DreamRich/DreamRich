"""
All attributes of this file have the annual order of magnitude
"""
from django.db import models


class GoalType(models.Model):
    name = models.CharField(max_length=100)


class GoalManager(models.Model):

    @property
    def duration_goals(self):
        duration_goals = self.financialplanning.financial_independence.age

        return duration_goals


class Goal(models.Model):
    is_periodic = models.BooleanField()
    year_init = models.PositiveSmallIntegerField()
    year_end = models.PositiveSmallIntegerField()
    periodicity = models.PositiveSmallIntegerField()
    value = models.PositiveIntegerField()
    goal_manager = models.ForeignKey(
            GoalManager,
        on_delete=models.CASCADE
    )
    goal_type = models.ForeignKey(GoalType, on_delete=models.CASCADE)
