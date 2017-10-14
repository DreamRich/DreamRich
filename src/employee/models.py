from django.db import models
from dreamrich import validators
from client.models import ActiveClient
from dr_auth.models import BaseUser


class Employee(BaseUser):

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_cpf]
    )


class FinancialAdviser(Employee):
    clients = models.ManyToManyField(ActiveClient)
