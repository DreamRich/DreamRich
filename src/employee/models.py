from django.db import models
from dreamrich import validators
from client.models import ActiveClient
from dr_auth.models import BaseUser
from simple_history.models import HistoricalRecords


class Employee(BaseUser):

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_cpf]
    )

    history = HistoricalRecords()


class FinancialAdviser(Employee):
    clients = models.ManyToManyField(ActiveClient)

    history = HistoricalRecords()
