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
