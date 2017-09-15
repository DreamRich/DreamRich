from django.db import models
from client.models import ActiveClient
from patrimony.models import Patrimony


class FinancialPlanning(models.Model):

    active_client = models.OneToOneField(
        ActiveClient,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    partimony = models.OneToOneField(
        Patrimony,
        on_delete=models.CASCADE,
        primary_key=True,
    )
