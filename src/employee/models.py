from django.db import models
from dreamrich import validators
from client.models import ActiveClient
from dr_auth.models import BaseUser


class Employee(BaseUser):

    default_permissions = []

    cpf = models.CharField(
        max_length=14,
        validators=[validators.validate_cpf]
    )


class FinancialAdviser(Employee):

    default_permissions = []

    clients = models.ManyToManyField(
        ActiveClient,
        related_name='financial_advisers'
    )
