from django.db import models
from client.models import ActiveClient
from patrimony.models import Patrimony
from goal.models import GoalManager


class FinancialIndependence(models.Model):
    age = models.PositiveSmallIntegerField()
    duration_of_usufruct = models.PositiveSmallIntegerField()
    remain_patrimony = models.PositiveIntegerField()


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
