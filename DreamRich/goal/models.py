"""
All attributes of this file have the annual order of magnitude
"""
from django.db import models


class FinancialIndependence(models.Model):
    age = models.PositiveSmallIntegerField()
    duration_of_usufruct = models.PositiveSmallIntegerField()
    remain_patrimony = models.PositiveIntegerField()


class GoalType(models.Model):
    name = models.CharField(max_length=100)


class Goal(models.Model):
    is_periodic = models.BooleanField()
    year_init = models.PositiveSmallIntegerField()
    year_end = models.PositiveSmallIntegerField()
    periodicity = models.PositiveSmallIntegerField()
    value = models.PositiveIntegerField()
    financial_indepedence = models.ForeignKey(FinancialIndependence,
                                              on_delete=models.CASCADE)
    goal_type = models.ForeignKey(GoalType, on_delete=models.CASCADE)
