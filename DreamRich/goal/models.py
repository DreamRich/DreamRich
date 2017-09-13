"""
All attributes of this file have the annual order of magnitude
"""
from django.db import models


class FinancialIndependence(models.Model):
    age = models.PositiveSmallIntegerField()
    duration_of_usufruct = models.PositiveSmallIntegerField()
    remain_patrimony = models.PositiveIntegerField()


class Goal(models.Model):
    is_periodic = models.BooleanField()
    date_init = models.DateField()
    date_end = models.DateField()
    periodicity = models.PositiveSmallIntegerField()
    financial_indepedence = models.ForeignKey(FinancialIndependence,
                                              on_delete=models.CASCADE)


class GoalType(models.Model):
    name = models.CharField(max_length=100)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
